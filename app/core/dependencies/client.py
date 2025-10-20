from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.dependencies.admin import (
    get_category_progress_info_service,
    get_meaning_progress_info_service,
    get_definition_progress_info_service,
    get_level_service as get_level_service_admin,
)
from app.core.dependencies.common import (
    get_statistic_service,
    get_translation_service,
    get_issue_status_service,
)

from app.services.client import (
    CategoryService,
    QuestionService,
    LevelService,
    TranslateService,
    IssueService,
)

from app.services.common import TranslationService


async def get_translate_service(
    svc_translation: TranslationService = Depends(get_translation_service),
) -> TranslateService:
    return TranslateService(svc_translation=svc_translation)


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
    svc_level=Depends(get_level_service_admin),
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


async def get_issue_service(
    db: AsyncSession = Depends(get_db),
    svc_issue_status=Depends(get_issue_status_service),
) -> IssueService:
    return IssueService(db, svc_issue_status)
