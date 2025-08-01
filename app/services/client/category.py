from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_categories as crud_get_categories,
)
from app.schemas.client import CategoriesListResponse


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> CategoriesListResponse:
        return await crud_get_categories(self.db)
