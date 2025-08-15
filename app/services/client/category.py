from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_category as crud_get_category,
    get_categories as crud_get_categories,
)
from app.models import User
from app.schemas.client import CategoriesListResponse, CategoryOut
from app.services.admin import CategoryProgressInfoService


class CategoryService:
    def __init__(
        self, db: AsyncSession, svc_category_progress_info: CategoryProgressInfoService
    ):
        self.db = db
        self.svc_category_progress_info = svc_category_progress_info

    async def get(self, current_user: User, category_id: int) -> CategoryOut:
        category = await crud_get_category(self.db, category_id)
        cpi = await self.svc_category_progress_info.get_top_category_progress_info(
            user_id=current_user.id, category_id=category_id
        )

        if category is None:
            raise Exception("Category not found")

        return CategoryOut.from_model(category=category, level=cpi.level)

    async def get_all(self) -> CategoriesListResponse:
        return await crud_get_categories(self.db)
