from app.api.main import api_router
from tenacity import retry, stop_after_attempt, wait_fixed
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine, Base

from app.core.config import settings

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
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


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)
app.include_router(api_router, prefix=settings.API_V1_STR)
