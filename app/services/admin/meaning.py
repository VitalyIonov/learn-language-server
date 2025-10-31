from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.admin import (
    get_meaning as crud_get_meaning,
    update_meaning as crud_update_meaning,
    delete_meaning as crud_delete_meaning,
    create_meaning as crud_create_meaning,
    get_meanings as crud_get_meanings,
)
from app.schemas.admin import MeaningUpdate, MeaningCreate, MeaningsListResponse
from app.models.common import Meaning
from app.schemas.common import AudioAssetUpload
from .audio import AudioService


class MeaningService:
    def __init__(self, db: AsyncSession, svc_audio: AudioService):
        self.db = db
        self.svc_audio = svc_audio

    async def get(self, meaning_id: int) -> Meaning:
        entity = await crud_get_meaning(self.db, meaning_id)
        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Meaning not found"
            )
        return entity

    async def get_all(self, offset: int, limit: int, q: str) -> MeaningsListResponse:
        return await crud_get_meanings(self.db, offset, limit, q)

    async def create(self, payload: MeaningCreate) -> Meaning:
        return await crud_create_meaning(self.db, payload)

    async def update(self, meaning_id: int, payload: MeaningUpdate) -> Meaning:
        entity = await self.get(meaning_id)

        return await crud_update_meaning(self.db, entity, payload)

    async def delete(self, meaning_id: int) -> None:
        success = await crud_delete_meaning(self.db, meaning_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Meaning not found"
            )

    async def generate_audio(self, meaning_id: int):
        entity = await self.get(meaning_id)

        if entity.audio_id is not None:
            raise HTTPException(
                status_code=400, detail="Audio already generated for this definition"
            )

        result = await self.svc_audio.create(AudioAssetUpload(text=entity.name))

        return await self.update(meaning_id, MeaningUpdate(audio_id=result.audio_id))
