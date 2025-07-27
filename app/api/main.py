from fastapi import APIRouter

from app.api.routes import login, users, categories, levels, meanings, definitions

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(categories.router)
api_router.include_router(levels.router)
api_router.include_router(meanings.router)
api_router.include_router(definitions.router)
