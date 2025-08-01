from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.admin import (
    MeaningService,
    DefinitionService,
    LevelService,
    CategoryService,
)


async def get_meaning_service(db: AsyncSession = Depends(get_db)) -> MeaningService:
    return MeaningService(db)


async def get_definition_service(
    db: AsyncSession = Depends(get_db),
) -> DefinitionService:
    return DefinitionService(db)


async def get_level_service(db: AsyncSession = Depends(get_db)) -> LevelService:
    return LevelService(db)


async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)
