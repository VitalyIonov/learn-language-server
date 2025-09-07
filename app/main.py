from app.api.main import admin_router, auth_router, client_router
from tenacity import retry, stop_after_attempt, wait_fixed
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.db import engine, Base

from app.core.config import settings

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]


async def init_models():
    async with engine.connect() as conn:

        await conn.run_sync(Base.metadata.create_all)


@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
@asynccontextmanager
async def lifespan(_):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


admin_app = FastAPI(
    title="admin",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
)

admin_app.include_router(admin_router)
# admin_app.include_router(login_router, prefix=settings.API_V1_STR)

auth_app = FastAPI(
    title="auth API",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
)
auth_app.include_router(auth_router)

client_app = FastAPI(
    title="client API",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",
)

client_app.include_router(client_router)

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.mount(f"{settings.API_V1_STR}/client", client_app)
app.mount(f"{settings.API_V1_STR}/admin", admin_app)
app.mount(f"{settings.API_V1_STR}/auth", auth_app)
app.mount("/static", StaticFiles(directory="static"), name="static")
