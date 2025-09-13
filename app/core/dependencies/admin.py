from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.admin import (
    MeaningService,
    TextDefinitionService,
    ImageDefinitionService,
    LevelService,
    CategoryService,
    UserInfoService,
    CategoryProgressInfoService,
    MeaningProgressInfoService,
    DefinitionProgressInfoService,
    ImageService,
    StorageR2Service,
    QuestionTypeService,
    TTSService,
    AudioService,
)


async def get_image_definition_service(
    db: AsyncSession = Depends(get_db),
) -> ImageDefinitionService:
    return ImageDefinitionService(db)


async def get_level_service(db: AsyncSession = Depends(get_db)) -> LevelService:
    return LevelService(db)


async def get_storage_r2_service() -> StorageR2Service:
    return StorageR2Service()


async def get_category_service(
    db: AsyncSession = Depends(get_db),
) -> CategoryService:
    return CategoryService(db)


async def get_user_info_service(db: AsyncSession = Depends(get_db)) -> UserInfoService:
    return UserInfoService(db)


async def get_category_progress_info_service(
    db: AsyncSession = Depends(get_db),
    svc_level: LevelService = Depends(get_level_service),
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


async def get_question_type_service(
    db: AsyncSession = Depends(get_db),
) -> QuestionTypeService:
    return QuestionTypeService(db)


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
