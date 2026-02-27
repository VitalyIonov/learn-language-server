from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.common import User

from app.services.admin import (
    MeaningService,
    TextDefinitionService,
    ImageDefinitionService,
    LevelService as LevelServiceAdmin,
    CategoryService as CategoryServiceAdmin,
    UserInfoService,
    CategoryProgressInfoService,
    MeaningProgressInfoService,
    DefinitionProgressInfoService,
    ImageService,
    StorageR2Service,
    TTSService,
    AudioService,
    IssueService as IssueServiceAdmin,
)

from app.services.client import (
    CategoryService as CategoryServiceClient,
    QuestionService,
    StatisticService,
    LevelService as LevelServiceClient,
    IssueService as IssueServiceClient,
    SettingsService,
)

from app.services.common import (
    UserService,
    AuthService,
    TranslationService,
    IssueTypeService,
    IssueStatusService,
    TranslateService,
)
from app.core.dependencies.auth import oauth2_scheme


async def get_image_definition_service(
    db: AsyncSession = Depends(get_db),
) -> ImageDefinitionService:
    return ImageDefinitionService(db)


async def get_level_service_admin(
    db: AsyncSession = Depends(get_db),
) -> LevelServiceAdmin:
    return LevelServiceAdmin(db)


async def get_storage_r2_service() -> StorageR2Service:
    return StorageR2Service()


async def get_category_service_admin(
    db: AsyncSession = Depends(get_db),
) -> CategoryServiceAdmin:
    return CategoryServiceAdmin(db)


async def get_user_info_service(db: AsyncSession = Depends(get_db)) -> UserInfoService:
    return UserInfoService(db)


async def get_category_progress_info_service(
    db: AsyncSession = Depends(get_db),
    svc_level: LevelServiceAdmin = Depends(get_level_service_admin),
) -> CategoryProgressInfoService:
    return CategoryProgressInfoService(db=db, svc_level=svc_level)


async def get_meaning_progress_info_service(
    db: AsyncSession = Depends(get_db),
) -> MeaningProgressInfoService:
    return MeaningProgressInfoService(db)


async def get_definition_progress_info_service(
    db: AsyncSession = Depends(get_db),
) -> DefinitionProgressInfoService:
    return DefinitionProgressInfoService(db)


async def get_image_service(
    db: AsyncSession = Depends(get_db),
    svc_storage_r2: StorageR2Service = Depends(get_storage_r2_service),
) -> ImageService:
    return ImageService(db=db, svc_storage_r2=svc_storage_r2)


async def get_tts_service() -> TTSService:
    return TTSService()


async def get_audio_service(
    db: AsyncSession = Depends(get_db),
    svc_storage_r2: StorageR2Service = Depends(get_storage_r2_service),
    svc_tts: TTSService = Depends(get_tts_service),
) -> AudioService:
    return AudioService(db=db, svc_storage_r2=svc_storage_r2, svc_tts=svc_tts)


async def get_text_definition_service(
    db: AsyncSession = Depends(get_db),
    svc_audio: AudioService = Depends(get_audio_service),
) -> TextDefinitionService:
    return TextDefinitionService(db, svc_audio=svc_audio)


async def get_meaning_service(
    db: AsyncSession = Depends(get_db),
    svc_audio: AudioService = Depends(get_audio_service),
) -> MeaningService:
    return MeaningService(db, svc_audio=svc_audio)


async def get_issue_service_admin(
    db: AsyncSession = Depends(get_db),
) -> IssueServiceAdmin:
    return IssueServiceAdmin(db)


async def get_user_service(
    db: AsyncSession = Depends(get_db),
    svc_cpi: CategoryProgressInfoService = Depends(get_category_progress_info_service),
    svc_user_info: UserInfoService = Depends(get_user_info_service),
) -> UserService:
    return UserService(db, svc_cpi=svc_cpi, svc_user_info=svc_user_info)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_svc: UserService = Depends(get_user_service),
) -> User | None:
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


async def get_translate_service() -> TranslateService:
    return TranslateService()


def get_issue_type_service(db: AsyncSession = Depends(get_db)) -> IssueTypeService:
    return IssueTypeService(db)


def get_issue_status_service(db: AsyncSession = Depends(get_db)) -> IssueStatusService:
    return IssueStatusService(db)


async def get_category_service_client(
    db: AsyncSession = Depends(get_db),
    svc_category_progress_info=Depends(get_category_progress_info_service),
) -> CategoryServiceClient:
    return CategoryServiceClient(
        db=db, svc_category_progress_info=svc_category_progress_info
    )


async def get_question_service(
    db: AsyncSession = Depends(get_db),
    svc_category_progress_info=Depends(get_category_progress_info_service),
    svc_meaning_progress_info=Depends(get_meaning_progress_info_service),
    svc_definition_progress_info=Depends(get_definition_progress_info_service),
    svc_statistic=Depends(get_statistic_service),
) -> QuestionService:
    return QuestionService(
        db=db,
        svc_category_progress_info=svc_category_progress_info,
        svc_meaning_progress_info=svc_meaning_progress_info,
        svc_definition_progress_info=svc_definition_progress_info,
        svc_statistic=svc_statistic,
    )


async def get_level_service_client(
    db: AsyncSession = Depends(get_db),
) -> LevelServiceClient:
    return LevelServiceClient(db)


async def get_issue_service_client(
    db: AsyncSession = Depends(get_db),
    svc_issue_status=Depends(get_issue_status_service),
) -> IssueServiceClient:
    return IssueServiceClient(db, svc_issue_status)


async def get_translation_service(
    db: AsyncSession = Depends(get_db),
    svc_translate: TranslateService = Depends(get_translate_service),
) -> TranslationService:
    return TranslationService(db, svc_translate)


async def get_settings_service(
    db: AsyncSession = Depends(get_db),
) -> SettingsService:
    return SettingsService(db)
