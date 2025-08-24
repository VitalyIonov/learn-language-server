from fastapi import HTTPException
from sqlalchemy import select, literal, exists
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.exc import NoResultFound

from app.models import Level, Category
from app.models.common import CategoryProgressInfo
from app.schemas.admin import (
    CategoryProgressInfoCreate,
    CategoryProgressInfoUpdate,
    UpdateCategoryLevelResult,
)
from app.crud.admin import (
    get_category_progress_info as crud_get_category_progress_info,
    create_category_progress_info as crud_create_category_progress_info,
    update_category_progress_info as crud_update_category_progress_info,
    get_top_category_progress_info as crud_get_top_category_progress_info,
)
from app.services.admin import LevelService


class CategoryProgressInfoService:
    def __init__(
        self,
        db: AsyncSession,
        svc_level: LevelService,
    ):
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

        # toDo | Удалить! Подумать как инициализировать при создании пользователя
        if cpi is None:
            level = await self.svc_level.get_first_level()

            cpi = (
                await self.get_or_create(
                    user_id=user_id, category_id=category_id, level_id=level.id
                )
                if level
                else None
            )

        if cpi is None:
            raise NoResultFound("CategoryProgressInfo non found")

        return cpi

    async def update_category_level(
        self,
        user_id: int,
        category_id: int,
        current_level_id: int,
    ) -> UpdateCategoryLevelResult:
        next_level = await self.svc_level.get_next_level(current_level_id)

        if next_level is None:
            return UpdateCategoryLevelResult()

        next_cpi = await self.get(
            user_id=user_id, category_id=category_id, level_id=next_level.id
        )

        if next_cpi is not None:
            return UpdateCategoryLevelResult(next_level=next_level)

        new_next_cpi = await self.create(
            CategoryProgressInfoCreate(
                user_id=user_id, category_id=category_id, level_id=next_level.id
            )
        )

        return UpdateCategoryLevelResult(
            next_level=next_level, new_next_cpi=new_next_cpi
        )

    async def bootstrap(self, user_id: int) -> None:
        first_level_sq = select(Level.id).order_by(Level.value).limit(1).subquery()

        stmt = (
            insert(CategoryProgressInfo)
            .from_select(
                ["user_id", "category_id", "level_id"],
                select(
                    literal(user_id),
                    Category.id,
                    first_level_sq.c.id,
                )
                .select_from(Category.__table__)
                .where(
                    ~exists().where(
                        (CategoryProgressInfo.user_id == user_id)
                        & (CategoryProgressInfo.category_id == Category.id)
                        & (CategoryProgressInfo.level_id == first_level_sq.c.id)
                    )
                ),
            )
            .on_conflict_do_nothing(
                index_elements=["user_id", "category_id", "level_id"]
            )
        )

        await self.db.execute(stmt)
