from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.level import (
    get_levels as crud_get_levels,
    create_level as crud_create_level,
)

from app.models.level import Level
from app.schemas import LevelCreate, LevelsListResponse


class LevelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, offset: int, limit: int, q: str) -> LevelsListResponse:
        return await crud_get_levels(self.db, offset, limit, q)

    async def create(self, payload: LevelCreate) -> Level:
        return await crud_create_level(self.db, payload)
