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
        file_key = make_tts_hash(payload.text)

        audio = await self._get_existing_audio(file_key)

        if audio:
            return AudioAssetUploadOut(audio_id=audio.id)

        is_file_exists = await self.svc_storage_r2.file_exists(file_key)

        if is_file_exists:
            audio = await self._create_audio_from_existing_file(file_key)
        else:
            audio = await self._create_audio_with_synthesis(payload.text, file_key)

        if audio is None:
            raise HTTPException(
                status_code=500, detail="Не удалось создать аудио-ассет"
            )

        return AudioAssetUploadOut(audio_id=audio.id)

    async def _get_existing_audio(self, file_key: str) -> AudioAsset | None:
        audio = await self.get_by_file_key(file_key)

        if audio is not None and audio.status == AssetStatus.READY:
            return audio

        return None

    async def _create_audio_from_existing_file(
        self, file_key: str
    ) -> AudioAsset | None:
        file_metadata = await self.svc_storage_r2.get_file_metadata(file_key)
        if not file_metadata:
            print(f"Не удалось получить метаданные файла {file_key} из R2")
            return None

        try:
            audio = await crud_create_audio(
                self.db,
                AudioAssetCreate(
                    mime_type=file_metadata.get("content_type", "audio/mpeg"),
                    size_bytes=file_metadata.get("content_length", 0),
                    file_key=file_key,
                ),
            )

            if audio:
                await self.commit(audio.id)
                return audio
            return None
        except Exception as e:
            print(f"Ошибка при создании записи аудио в БД: {e}")
            return None

    async def _create_audio_with_synthesis(
        self, text: str, file_key: str
    ) -> AudioAsset | None:
        try:
            file_obj = await self.svc_tts.synthesize(TTSGenerate(text=text))
            if not file_obj or not file_obj.data:
                print(f"Не удалось синтезировать аудио для текста: {text}")
                return None

            audio = await crud_create_audio(
                self.db,
                AudioAssetCreate(
                    mime_type=file_obj.content_type,
                    size_bytes=len(file_obj.data),
                    file_key=file_key,
                ),
            )

            if not audio:
                print(f"Не удалось создать запись аудио в БД для ключа {file_key}")
                return None

            upload_success = await self.svc_storage_r2.upload_file(
                audio.file_key, io.BytesIO(file_obj.data), file_obj.content_type
            )

            if upload_success:
                await self.commit(audio.id)
                return audio
            else:
                print(f"Не удалось загрузить аудио в R2 для ключа {file_key}")
                return None

        except Exception as e:
            print(f"Ошибка при создании аудио с синтезом: {e}")
            return None

    async def commit(self, audio_id: int) -> AudioAsset:
        audio = await self.get(audio_id)

        if audio.status == AssetStatus.READY:
            return audio

        return await crud_update_audio(
            self.db, audio, AudioAssetUpdate(status=AssetStatus.READY)
        )
