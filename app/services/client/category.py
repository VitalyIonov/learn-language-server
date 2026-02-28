from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_category as crud_get_category,
    get_categories as crud_get_categories,
)
from app.schemas.client import CategoriesListResponse, CategoryOut


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, category_id: int) -> CategoryOut:
        category = await crud_get_category(self.db, category_id=category_id)

        if category is None:
            raise NoResultFound("Category not found")

        return CategoryOut.model_validate(category)

    async def get_all(self) -> CategoriesListResponse:
        return await crud_get_categories(self.db)
