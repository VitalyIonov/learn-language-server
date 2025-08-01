from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.admin import (
    get_categories as crud_get_categories,
    create_category as crud_create_category,
)
from app.models.common import Category
from app.schemas.admin import CategoryCreate, CategoriesListResponse


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, offset: int, limit: int, q: str) -> CategoriesListResponse:
        return await crud_get_categories(self.db, offset, limit, q)

    async def create(self, payload: CategoryCreate) -> Category:
        return await crud_create_category(self.db, payload)
