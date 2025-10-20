from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.admin import (
    get_category_progress_info_service,
    get_user_info_service,
)
from app.models.common import User
from app.core.db import get_db
from app.services.admin import CategoryProgressInfoService, UserInfoService
from app.services.common import (
    UserService,
    AuthService,
    StatisticService,
    TranslationService,
    IssueTypeService,
    IssueStatusService,
)
from app.core.dependencies.auth import oauth2_scheme


async def get_user_service(
    db: AsyncSession = Depends(get_db),
    svc_cpi: CategoryProgressInfoService = Depends(get_category_progress_info_service),
    svc_user_info: UserInfoService = Depends(get_user_info_service),
) -> UserService:
    return UserService(db, svc_cpi=svc_cpi, svc_user_info=svc_user_info)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_svc: UserService = Depends(get_user_service),
) -> User:
    email = AuthService.decode_token(token)
    return await user_svc.get_by_email(email)


async def require_admin(
    current_user: User = Depends(get_current_user),
    user_svc: UserService = Depends(get_user_service),
) -> User:
    await user_svc.require_admin(current_user)
    return current_user


def get_statistic_service(db: AsyncSession = Depends(get_db)) -> StatisticService:
    return StatisticService(db)


def get_translation_service(db: AsyncSession = Depends(get_db)) -> TranslationService:
    return TranslationService(db)


def get_issue_type_service(db: AsyncSession = Depends(get_db)) -> IssueTypeService:
    return IssueTypeService(db)


def get_issue_status_service(db: AsyncSession = Depends(get_db)) -> IssueStatusService:
    return IssueStatusService(db)
