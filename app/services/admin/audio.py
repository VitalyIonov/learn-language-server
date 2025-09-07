from fastapi import HTTPException
import io

from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import make_tts_hash

from app.crud.admin import (
    get_audio as crud_get_audio,
    get_audio_by_file_key as crud_get_audio_by_file_key,
    create_audio as crud_create_audio,
    update_audio as crud_update_audio,
)
from app.models import AudioAsset, AssetStatus
from app.schemas.admin import TTSGenerate
from app.schemas.common import (
    AudioAssetUpload,
    AudioAssetUploadOut,
    AudioAssetCreate,
    AudioAssetUpdate,
)
from .storage_r2 import StorageR2Service
from .tts import TTSService


class AudioService:
    def __init__(
        self, db: AsyncSession, svc_storage_r2: StorageR2Service, svc_tts: TTSService
    ):
        self.db = db
        self.svc_storage_r2 = svc_storage_r2
        self.svc_tts = svc_tts

    async def get(self, audio_id: int) -> AudioAsset:
        entity = await crud_get_audio(self.db, audio_id)

        if entity is None:
            raise HTTPException(404, "Audio not found")

        return entity

    async def get_by_file_key(self, file_key: str) -> AudioAsset | None:
        return await crud_get_audio_by_file_key(self.db, file_key)

    async def create(self, payload: AudioAssetUpload) -> AudioAssetUploadOut:
        file_obj = await self.svc_tts.synthesize(TTSGenerate(text=payload.text))
        file_key = make_tts_hash(payload.text)

        audio = await self.get_by_file_key(file_key)

        if audio is not None and audio.status == AssetStatus.READY:
            return AudioAssetUploadOut(audio_id=audio.id)

        if audio is None:
            audio = await crud_create_audio(
                self.db,
                AudioAssetCreate(
                    mime_type=file_obj.content_type,
                    size_bytes=len(file_obj.data),
                    file_key=file_key,
                ),
            )

        upload_success = await self.svc_storage_r2.upload_file(
            audio.file_key, io.BytesIO(file_obj.data), file_obj.content_type
        )

        if upload_success:
            await self.commit(audio.id)

        return AudioAssetUploadOut(audio_id=audio.id)

    async def commit(self, audio_id: int) -> AudioAsset:
        audio = await self.get(audio_id)

        if audio.status == AssetStatus.READY:
            return audio

        return await crud_update_audio(
            self.db, audio, AudioAssetUpdate(status=AssetStatus.READY)
        )
