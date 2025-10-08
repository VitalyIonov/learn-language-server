import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from openai import OpenAI

from app.services.common import TranslationService

DEEPL_API_KEY = settings.DEEPL_API_KEY
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-mini"


class TranslateService:
    def __init__(self, svc_translation: TranslationService):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.svc_translation = svc_translation

    @staticmethod
    def translate_by_deepl(
        text: str, lang_from: str = "ES", lang_to: str = "RU"
    ) -> str:
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' parameter")

        headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
        data = {
            "text": text,
            "source_lang": lang_from,
            "target_lang": lang_to,
        }

        try:
            resp = httpx.post(DEEPL_API_URL, data=data, headers=headers, timeout=15)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"DeepL API error: {str(e)}")

        result = resp.json()
        return result["translations"][0]["text"]

    async def translate_by_open_ai(
        self, text: str, lang_from: str = "ES", lang_to: str = "RU"
    ) -> str:
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' parameter")

        translated_text = await self.svc_translation.get(text, lang_from, lang_to)

        if translated_text:
            return translated_text

        open_ai_response = self._client.responses.create(
            model=DEFAULT_TRANSLATION_MODEL,
            instructions=(
                "Ты профессиональный переводчик. Переводи строго с испанского на русский. "
                "Выводи ТОЛЬКО перевод — без кавычек, без пояснений, без префиксов. "
                "Сохраняй числовые форматы, эмодзи и разметку."
            ),
            input=f"Стиль: нейтрально-разговорно.\n\nТекст:\n{text}",
            temperature=0.1,
            max_output_tokens=2000,
        )

        open_ai_response_translation = (open_ai_response.output_text or "").strip()

        translated_text = await self.svc_translation.create(
            text, open_ai_response_translation, lang_from, lang_to
        )

        return translated_text
