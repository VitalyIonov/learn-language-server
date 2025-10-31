import httpx
from fastapi import HTTPException

from app.core.config import settings

from openai import OpenAI

DEEPL_API_KEY = settings.DEEPL_API_KEY
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEFAULT_TRANSLATION_MODEL = "gpt-4o-mini"

_LANG_MAP = {
    "es": "Spanish",
    "ru": "Russian",
    "en": "English",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "it": "Italian",
}


def _normalize_lang(lang: str) -> str:
    if not lang:
        return ""
    key = lang.strip().lower()
    return _LANG_MAP.get(key, lang.strip().title())


ACTION_STYLE_BY_LANG: dict[str, str] = {
    "ru": (
        "Передавай действие в процессе: используй глаголы несовершенного вида "
        "(отвечающие на вопрос «что делает?»), где это уместно. "
        "Напр.: «afeitarse» → «бриться», «lavar los platos» → «мыть посуду»."
    ),
    "en": (
        "Prefer action-as-process phrasing (present simple or gerund where natural), "
        "e.g., “to shave” / “shaving”, “to wash the dishes” / “washing the dishes”."
    ),
    "es": (
        "Usa el infinitivo para expresar la acción de forma general, "
        "p. ej., «afeitarse», «lavar los platos», «leer un libro»."
    ),
}

BASE_RULES = (
    "Выводи ТОЛЬКО перевод — без кавычек, пояснений и префиксов. "
    "Сохраняй числовые форматы, эмодзи и разметку."
)


def build_instructions(lang_from: str, lang_to: str) -> str:
    style = ACTION_STYLE_BY_LANG.get(lang_to)
    return (
        f"Ты переводчик. Переводи строго с {lang_from} на {lang_to}. "
        f"{style} {BASE_RULES}"
    ).strip()


class TranslateService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
        self,
        text: str,
        lang_from: str = "ES",
        lang_to: str = "RU",
        context: str | None = None,
    ) -> str:
        src = _normalize_lang(lang_from)
        dst = _normalize_lang(lang_to)

        if context:
            user_input = (
                "Стиль: нейтрально-разговорно.\n\n"
                "CONTEXT (do not translate):\n"
                "-----\n"
                f"{context}\n"
                "-----\n\n"
                "TEXT (translate only this):\n"
                f"{text}"
            )
        else:
            user_input = (
                "Стиль: нейтрально-разговорно.\n\n"
                "TEXT (translate only this):\n"
                f"{text}"
            )

        instructions = build_instructions(src, dst)

        open_ai_response = self._client.responses.create(
            model=DEFAULT_TRANSLATION_MODEL,
            instructions=instructions,
            input=user_input,
            temperature=0.1,
            max_output_tokens=2000,
        )

        return (open_ai_response.output_text or "").strip()
