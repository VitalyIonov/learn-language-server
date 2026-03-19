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
    EmbeddingService,
    TranslationService,
    TranslateService,
    TranslationValidatorService,
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
) -> UserService:
    return UserService(db)


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


async def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


async def get_translation_validator_service() -> TranslationValidatorService:
    return TranslationValidatorService()


async def get_translate_service(
    svc_validator: TranslationValidatorService = Depends(get_translation_validator_service),
) -> TranslateService:
    return TranslateService(svc_validator=svc_validator)


async def get_question_service(
    db: AsyncSession = Depends(get_db),
    svc_meaning_progress_info=Depends(get_meaning_progress_info_service),
    svc_definition_progress_info=Depends(get_definition_progress_info_service),
) -> QuestionService:
    return QuestionService(
        db=db,
        svc_meaning_progress_info=svc_meaning_progress_info,
        svc_definition_progress_info=svc_definition_progress_info,
    )


async def get_issue_service_client(
    db: AsyncSession = Depends(get_db),
) -> IssueServiceClient:
    return IssueServiceClient(db)


async def get_translation_service(
    db: AsyncSession = Depends(get_db),
    svc_translate: TranslateService = Depends(get_translate_service),
    svc_validator: TranslationValidatorService = Depends(get_translation_validator_service),
) -> TranslationService:
    return TranslationService(db, svc_translate=svc_translate, svc_validator=svc_validator)


async def get_category_service_client(
    db: AsyncSession = Depends(get_db),
    svc_translation: TranslationService = Depends(get_translation_service),
) -> CategoryServiceClient:
    return CategoryServiceClient(db=db, svc_translation=svc_translation)


async def get_level_service_client(
    db: AsyncSession = Depends(get_db),
    svc_translation: TranslationService = Depends(get_translation_service),
) -> LevelServiceClient:
    return LevelServiceClient(db, svc_translation=svc_translation)


async def get_settings_service(
    db: AsyncSession = Depends(get_db),
) -> SettingsService:
    return SettingsService(db)
