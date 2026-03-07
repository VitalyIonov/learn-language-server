import json
import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings

from openai import OpenAI

logger = logging.getLogger(__name__)

DEEPL_API_KEY = settings.DEEPL_API_KEY
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEFAULT_TRANSLATION_MODEL = "gpt-4o"

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
        "Для описаний действий используй глаголы несовершенного вида "
        "(отвечающие на вопрос «что делает?»). "
        "Напр.: «afeitarse» → «бриться», «lavar los platos» → «мыть посуду». "
        "Существительные и названия предметов оставляй существительными "
        "(напр.: «razor» → «бритва», не «бриться»)."
    ),
    "en": (
        "For action descriptions, prefer present simple or gerund where natural, "
        'e.g., "to shave" / "shaving", "to wash the dishes" / "washing the dishes". '
        "Nouns and object names must remain as nouns "
        '(e.g., "бритва" -> "razor", not "shaving").'
    ),
    "es": (
        "Para descripciones de acciones, usa el infinitivo "
        "(p. ej., «afeitarse», «lavar los platos»). "
        "Los sustantivos y nombres de objetos deben permanecer como sustantivos "
        "(p. ej., «бритва» → «maquinilla de afeitar», no «afeitarse»)."
    ),
}

BASE_RULES = "Выводи ТОЛЬКО перевод — без кавычек, пояснений и префиксов. " "Сохраняй числовые форматы, эмодзи и разметку."


def build_instructions(lang_from: str, lang_to: str) -> str:
    style = ACTION_STYLE_BY_LANG.get(lang_to)
    return f"Ты переводчик. Переводи строго с {lang_from} на {lang_to}. " f"{style} {BASE_RULES}".strip()


BATCH_OUTPUT_RULES = (
    "Верни ТОЛЬКО валидный JSON-массив вида "
    '[{"id": 0, "text": "перевод"}, ...]. '
    "Без markdown-обёртки, без пояснений, без кавычек вокруг массива."
)


def build_batch_instructions(lang_from: str, lang_to: str) -> str:
    style = ACTION_STYLE_BY_LANG.get(lang_to)
    return (
        f"Ты переводчик. Переводи строго с {lang_from} на {lang_to}. "
        f"{style} "
        "Сохраняй числовые форматы, эмодзи и разметку. "
        f"{BATCH_OUTPUT_RULES}"
    ).strip()


class TranslateService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def translate_by_deepl(text: str, lang_from: str = "ES", lang_to: str = "RU") -> str:
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
            user_input = "Стиль: нейтрально-разговорно.\n\n" "TEXT (translate only this):\n" f"{text}"

        instructions = build_instructions(src, dst)

        open_ai_response = self._client.responses.create(
            model=DEFAULT_TRANSLATION_MODEL,
            instructions=instructions,
            input=user_input,
            temperature=0.1,
            max_output_tokens=2000,
        )

        return (open_ai_response.output_text or "").strip()

    async def translate_batch_by_open_ai(
        self,
        texts: list[str],
        lang_to: str,
        lang_from: str = "ES",
        context: str | None = None,
        chunk_size: int = 25,
    ) -> list[str]:
        if not texts or not lang_to:
            return []

        src = _normalize_lang(lang_from)
        dst = _normalize_lang(lang_to)
        instructions = build_batch_instructions(src, dst)

        results: list[str] = []

        for chunk_start in range(0, len(texts), chunk_size):
            chunk = texts[chunk_start : chunk_start + chunk_size]
            items = [{"id": index, "text": text} for index, text in enumerate(chunk)]
            items_json = json.dumps(items, ensure_ascii=False)

            if context:
                user_input = (
                    "Стиль: нейтрально-разговорно.\n\n"
                    "CONTEXT (do not translate):\n"
                    "-----\n"
                    f"{context}\n"
                    "-----\n\n"
                    "Переведи каждый элемент массива. "
                    "Верни JSON-массив в том же формате.\n\n"
                    f"{items_json}"
                )
            else:
                user_input = (
                    "Стиль: нейтрально-разговорно.\n\n"
                    "Переведи каждый элемент массива. "
                    "Верни JSON-массив в том же формате.\n\n"
                    f"{items_json}"
                )

            try:
                chunk_results = await self._translate_batch_chunk(
                    instructions=instructions,
                    user_input=user_input,
                    expected_count=len(chunk),
                )
                results.extend(chunk_results)
            except Exception:
                logger.warning(
                    "Batch translation failed for chunk %d-%d, " "falling back to individual translations",
                    chunk_start,
                    chunk_start + len(chunk),
                    exc_info=True,
                )
                for text in chunk:
                    translated = await self.translate_by_open_ai(
                        text=text,
                        lang_from=lang_from,
                        lang_to=lang_to,
                        context=context,
                    )
                    results.append(translated)

        return results

    async def _translate_batch_chunk(
        self,
        instructions: str,
        user_input: str,
        expected_count: int,
    ) -> list[str]:
        open_ai_response = self._client.responses.create(
            model=DEFAULT_TRANSLATION_MODEL,
            instructions=instructions,
            input=user_input,
            temperature=0.1,
            max_output_tokens=4000,
        )

        raw = (open_ai_response.output_text or "").strip()

        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3].strip()

        parsed = json.loads(raw)
        sorted_items = sorted(parsed, key=lambda item: item["id"])

        if len(sorted_items) != expected_count:
            raise ValueError(f"Expected {expected_count} translations, " f"got {len(sorted_items)}")

        return [item["text"] for item in sorted_items]
