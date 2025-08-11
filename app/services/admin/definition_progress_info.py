from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.common import DefinitionProgressInfo
from app.schemas.admin import DefinitionProgressInfoCreate, DefinitionProgressInfoUpdate
from app.crud.admin import (
    get_definition_progress_info as crud_get_definition_progress_info,
    create_definition_progress_info as crud_create_definition_progress_info,
    update_definition_progress_info as crud_update_definition_progress_info,
)


class DefinitionProgressInfoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(
        self, user_id: int, meaning_id: int, definition_id: int
    ) -> DefinitionProgressInfo | None:
        return await crud_get_definition_progress_info(
            self.db, user_id, meaning_id, definition_id
        )

    async def create(
        self, payload: DefinitionProgressInfoCreate
    ) -> DefinitionProgressInfo:
        entity = await self.get(
            payload.user_id, payload.meaning_id, payload.definition_id
        )

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DefinitionProgressInfo already created",
            )

        return await crud_create_definition_progress_info(self.db, payload)

    async def update(
        self,
        user_id: int,
        meaning_id: int,
        definition_id: int,
        payload: DefinitionProgressInfoUpdate,
    ) -> DefinitionProgressInfo:
        entity = await self.get(user_id, meaning_id, definition_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="DefinitionProgressInfo not found",
            )

        return await crud_update_definition_progress_info(self.db, entity, payload)
