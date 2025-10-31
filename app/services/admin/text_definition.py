from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.admin import (
    TextDefinitionUpdate,
    TextDefinitionListResponse,
    TextDefinitionCreate,
)
from app.crud.admin import (
    get_text_definition as get_definition_crud,
    get_text_definitions as get_definitions_crud,
    create_text_definition as create_definition_crud,
    update_text_definition as update_definition_crud,
    delete_text_definition as delete_definition_crud,
)

from app.models.common import TextDefinition
from app.schemas.common import AudioAssetUpload
from .audio import AudioService


class TextDefinitionService:
    def __init__(self, db: AsyncSession, svc_audio: AudioService):
        self.db = db
        self.svc_audio = svc_audio

    async def get(self, definition_id: int) -> TextDefinition:
        result = await get_definition_crud(self.db, definition_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Definition not found")
        return result

    async def get_all(
        self, offset: int, limit: int, q: str
    ) -> TextDefinitionListResponse:
        return await get_definitions_crud(self.db, offset, limit, q)

    async def update(self, definition_id: int, payload: TextDefinitionUpdate):
        result = await get_definition_crud(self.db, definition_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Definition not found")
        return await update_definition_crud(self.db, result, payload)

    async def create(self, payload: TextDefinitionCreate) -> TextDefinition:
        return await create_definition_crud(self.db, payload)

    async def delete(self, definition_id: int):
        success = await delete_definition_crud(self.db, definition_id)
        if not success:
            raise HTTPException(status_code=404, detail="Definition not found")

    async def generate_audio(self, definition_id: int):
        entity = await self.get(definition_id)

        if entity.audio_id is not None:
            raise HTTPException(
                status_code=400, detail="Audio already generated for this definition"
            )

        result = await self.svc_audio.create(AudioAssetUpload(text=entity.text))

        return await self.update(
            definition_id, TextDefinitionUpdate(audio_id=result.audio_id)
        )
