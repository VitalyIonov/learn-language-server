from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.client import (
    CategoryService,
)


async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
