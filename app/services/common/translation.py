from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.common import (
    get_translation as crud_get_translation,
    create_translation as crud_create_translation,
)
from app.schemas.common import TranslationCreate


class TranslationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, text: str, lang_from: str, lang_to: str) -> Optional[str]:
        result = await crud_get_translation(self.db, text, lang_from, lang_to)

        return result.translated_text if result else None

    async def create(
        self, text: str, translated_text, lang_from: str, lang_to: str
    ) -> str:
        result = await crud_create_translation(
            self.db,
            TranslationCreate(
                text=text,
                translated_text=translated_text,
                lang_from=lang_from,
                lang_to=lang_to,
            ),
        )

        return result.translated_text
