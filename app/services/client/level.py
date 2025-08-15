from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_levels as crud_get_levels,
)

from app.schemas.client import LevelsListResponse


class LevelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int, category_id: int) -> LevelsListResponse:
        return await crud_get_levels(self.db, user_id=user_id, category_id=category_id)
