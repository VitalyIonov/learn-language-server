from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.dependencies.admin import (
    get_category_progress_info_service,
    get_meaning_progress_info_service,
    get_definition_progress_info_service,
    get_level_service,
)
from app.core.dependencies.common import get_statistic_service

from app.services.client import CategoryService, QuestionService, LevelService


async def get_category_service(
    db: AsyncSession = Depends(get_db),
    svc_category_progress_info=Depends(get_category_progress_info_service),
) -> CategoryService:
    return CategoryService(db=db, svc_category_progress_info=svc_category_progress_info)


async def get_question_service(
    db: AsyncSession = Depends(get_db),
    svc_category_progress_info=Depends(get_category_progress_info_service),
    svc_meaning_progress_info=Depends(get_meaning_progress_info_service),
    svc_definition_progress_info=Depends(get_definition_progress_info_service),
    svc_statistic=Depends(get_statistic_service),
    svc_level=Depends(get_level_service),
) -> QuestionService:
    return QuestionService(
        db=db,
        svc_category_progress_info=svc_category_progress_info,
        svc_meaning_progress_info=svc_meaning_progress_info,
        svc_definition_progress_info=svc_definition_progress_info,
        svc_statistic=svc_statistic,
        svc_level=svc_level,
    )


async def get_level_service(db: AsyncSession = Depends(get_db)) -> LevelService:
    return LevelService(db)
