from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.admin import (
    get_categories as crud_get_categories,
    create_category as crud_create_category,
    get_category as crud_get_category,
    update_category as crud_update_category,
    delete_category as crud_delete_category,
)
from app.models.common import Category
from app.schemas.admin import CategoryCreate, CategoriesListResponse, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, category_id: int) -> Category:
        entity = await crud_get_category(self.db, category_id)

        if entity is None:
            raise Exception("Category not found")

        return entity

    async def get_all(self, offset: int, limit: int, q: str) -> CategoriesListResponse:
        return await crud_get_categories(self.db, offset, limit, q)

    async def create(self, payload: CategoryCreate) -> Category:
        return await crud_create_category(self.db, payload)

    async def update(self, category_id: int, payload: CategoryUpdate) -> Category:
        entity = await self.get(category_id)
        return await crud_update_category(self.db, entity, payload)

    async def delete(self, category_id: int) -> None:
        success = await crud_delete_category(self.db, category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
