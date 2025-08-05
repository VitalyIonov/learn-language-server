from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.common import CategoryProgressInfo
from app.schemas.admin import CategoryProgressInfoCreate, CategoryProgressInfoUpdate
from app.crud.admin import (
    get_category_progress_info as crud_get_category_progress_info,
    create_category_progress_info as crud_create_category_progress_info,
    update_category_progress_info as crud_update_category_progress_info,
)


class CategoryProgressInfoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int, category_id: int) -> CategoryProgressInfo:
        entity = await crud_get_category_progress_info(self.db, user_id, category_id)
        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CategoryProgressInfo not found",
            )
        return entity

    async def create(self, payload: CategoryProgressInfoCreate) -> None:
        entity = await crud_get_category_progress_info(
            self.db, payload.user_id, payload.category_id
        )

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CategoryProgressInfo already created",
            )

        await crud_create_category_progress_info(self.db, payload)

    async def update(
        self, user_id: int, category_id: int, payload: CategoryProgressInfoUpdate
    ) -> CategoryProgressInfo:
        entity = await self.get(user_id, category_id)

        return await crud_update_category_progress_info(self.db, entity, payload)
