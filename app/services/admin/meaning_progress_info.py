from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.common import MeaningProgressInfo
from app.schemas.admin import MeaningProgressInfoCreate, MeaningProgressInfoUpdate
from app.crud.admin import (
    get_meaning_progress_info as crud_get_meaning_progress_info,
    create_meaning_progress_info as crud_create_meaning_progress_info,
    update_meaning_progress_info as crud_update_meaning_progress_info,
)


class MeaningProgressInfoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(
        self, user_id: int, meaning_id: int, level_id: int
    ) -> MeaningProgressInfo | None:
        return await crud_get_meaning_progress_info(
            self.db, user_id, meaning_id, level_id
        )

    async def create(self, payload: MeaningProgressInfoCreate) -> MeaningProgressInfo:
        entity = await self.get(payload.user_id, payload.meaning_id, payload.level_id)

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MeaningProgressInfo already created",
            )

        return await crud_create_meaning_progress_info(self.db, payload)

    async def update(
        self,
        user_id: int,
        meaning_id: int,
        level_id: int,
        payload: MeaningProgressInfoUpdate,
    ) -> MeaningProgressInfo:
        entity = await self.get(user_id, meaning_id, level_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MeaningProgressInfo not found",
            )

        return await crud_update_meaning_progress_info(self.db, entity, payload)

    async def get_or_create(
        self, user_id: int, meaning_id: int, level_id: int
    ) -> MeaningProgressInfo:
        entity = await self.get(user_id, meaning_id, level_id)

        if entity is None:
            entity = await self.create(
                MeaningProgressInfoCreate(
                    user_id=user_id,
                    meaning_id=meaning_id,
                    level_id=level_id,
                )
            )

        return entity
