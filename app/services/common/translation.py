from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.common import (
    get_translation as crud_get_translation,
    create_translation as crud_create_translation,
)
from app.schemas.common import TranslationCreate
from ..common.translate import TranslateService


class TranslationService:
    def __init__(
        self,
        db: AsyncSession,
        svc_translate: TranslateService,
    ):
        self.db = db
        self.svc_translate = svc_translate

    async def get(self, text: str, lang_from: str, lang_to: str) -> Optional[str]:
        result = await crud_get_translation(
            self.db, text=text, lang_from=lang_from, lang_to=lang_to
        )

        return result.translated_text if result else None

    async def create(
        self,
        text: str,
        translated_text,
        lang_from: str,
        lang_to: str,
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

    async def translate(
        self,
        text: str,
        lang_from: str = "es",
        lang_to: str = "ru",
        context: str | None = None,
    ) -> str:
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' parameter")

        translated_text = await self.get(text, lang_from, lang_to)

        if translated_text:
            return translated_text

        translated_text = await self.svc_translate.translate_by_open_ai(
            text, lang_from, lang_to, context=context
        )

        return await self.create(text, translated_text, lang_from, lang_to)
