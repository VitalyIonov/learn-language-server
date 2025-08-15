from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from sqlalchemy.exc import NoResultFound

from app.models.common import CategoryProgressInfo
from app.schemas.admin import CategoryProgressInfoCreate, CategoryProgressInfoUpdate
from app.crud.admin import (
    get_category_progress_info as crud_get_category_progress_info,
    create_category_progress_info as crud_create_category_progress_info,
    update_category_progress_info as crud_update_category_progress_info,
    get_top_category_progress_info as crud_get_top_category_progress_info,
)
from app.services.admin import LevelService


class CategoryProgressInfoService:
    def __init__(self, db: AsyncSession, svc_level: LevelService):
        self.db = db
        self.svc_level = svc_level

    async def get(
        self, user_id: int, category_id: int, level_id: int
    ) -> CategoryProgressInfo | None:
        return await crud_get_category_progress_info(
            self.db, user_id, category_id, level_id
        )

    async def create(self, payload: CategoryProgressInfoCreate) -> CategoryProgressInfo:
        entity = await self.get(payload.user_id, payload.category_id, payload.level_id)

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CategoryProgressInfo already created",
            )

        return await crud_create_category_progress_info(self.db, payload)

    async def update(
        self,
        user_id: int,
        category_id: int,
        level_id: int,
        payload: CategoryProgressInfoUpdate,
    ) -> CategoryProgressInfo:
        entity = await self.get(user_id, category_id, level_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CategoryProgressInfo not found",
            )

        return await crud_update_category_progress_info(self.db, entity, payload)

    async def get_or_create(
        self, user_id: int, category_id: int, level_id: int
    ) -> CategoryProgressInfo:
        entity = await self.get(
            user_id=user_id,
            category_id=category_id,
            level_id=level_id,
        )

        if entity is None:
            entity = await self.create(
                CategoryProgressInfoCreate(
                    user_id=user_id,
                    category_id=category_id,
                    level_id=level_id,
                )
            )

        return entity

    async def get_top_category_progress_info(
        self, user_id: int, category_id: int
    ) -> CategoryProgressInfo:
        cpi = await crud_get_top_category_progress_info(self.db, user_id, category_id)

        if cpi is None:
            raise NoResultFound("CategoryProgressInfo non found")

        return cpi

    async def update_category_level(
        self,
        user_id: int,
        category_id: int,
        current_level_id: int,
    ) -> CategoryProgressInfo | None:
        next_level = await self.svc_level.get_next_level(current_level_id)

        if next_level is None:
            return None

        entity = await self.get_or_create(
            user_id=user_id, category_id=category_id, level_id=next_level.id
        )

        return entity
