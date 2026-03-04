from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.constants.target_language import TargetLanguageCode
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
        self,
        user_id: int,
        meaning_id: int,
        level_id: int,
        language: TargetLanguageCode,
    ) -> MeaningProgressInfo | None:
        return await crud_get_meaning_progress_info(
            self.db,
            user_id=user_id,
            meaning_id=meaning_id,
            level_id=level_id,
            language=language,
        )

    async def create(self, payload: MeaningProgressInfoCreate) -> MeaningProgressInfo:
        entity = await self.get(
            user_id=payload.user_id,
            meaning_id=payload.meaning_id,
            level_id=payload.level_id,
            language=payload.language,
        )

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="MeaningProgressInfo already created",
            )

        return await crud_create_meaning_progress_info(self.db, payload=payload)

    async def update(
        self,
        user_id: int,
        meaning_id: int,
        level_id: int,
        language: TargetLanguageCode,
        payload: MeaningProgressInfoUpdate,
    ) -> MeaningProgressInfo:
        entity = await self.get(
            user_id=user_id,
            meaning_id=meaning_id,
            level_id=level_id,
            language=language,
        )

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="MeaningProgressInfo not found",
            )

        return await crud_update_meaning_progress_info(
            self.db, db_entity=entity, payload=payload,
        )

    async def get_or_create(
        self,
        user_id: int,
        meaning_id: int,
        level_id: int,
        category_id: int,
        language: TargetLanguageCode,
    ) -> MeaningProgressInfo:
        entity = await self.get(
            user_id=user_id,
            meaning_id=meaning_id,
            level_id=level_id,
            language=language,
        )

        if entity is None:
            entity = await self.create(
                MeaningProgressInfoCreate(
                    user_id=user_id,
                    meaning_id=meaning_id,
                    level_id=level_id,
                    category_id=category_id,
                    language=language,
                )
            )

        return entity
