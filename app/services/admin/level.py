from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.admin import (
    get_levels as crud_get_levels,
    create_level as crud_create_level,
    delete_level as crud_delete_level,
    get_next_level as crud_get_next_level,
)

from app.models.common import Level
from app.schemas.admin import LevelCreate, LevelsListResponse


class LevelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, offset: int, limit: int, q: str) -> LevelsListResponse:
        return await crud_get_levels(self.db, offset, limit, q)

    async def create(self, payload: LevelCreate) -> Level:
        return await crud_create_level(self.db, payload)

    async def delete(self, level_id: int) -> None:
        success = await crud_delete_level(self.db, level_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Level not found"
            )

    async def get_next_level(self, level_id: int) -> Optional[Level]:
        return await crud_get_next_level(self.db, level_id)
