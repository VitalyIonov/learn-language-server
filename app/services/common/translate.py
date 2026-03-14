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

from app.constants.translate import ACTION_STYLE, BASE_RULES, BATCH_OUTPUT_RULES


def build_instructions(lang_from: str, lang_to: str, group: str | None = None) -> str:
    style = ACTION_STYLE.get(lang_to, {}).get(group, "")
    parts = [
        f"Ты переводчик. Переводи строго с {lang_from} на {lang_to}.",
        style,
        BASE_RULES,
    ]
    return " ".join(part for part in parts if part).strip()


def build_batch_instructions(lang_from: str, lang_to: str, group: str | None = None) -> str:
    style = ACTION_STYLE.get(lang_to, {}).get(group, "")
    parts = [
        f"Ты переводчик. Переводи строго с {lang_from} на {lang_to}.",
        style,
        "Сохраняй числовые форматы, эмодзи и разметку.",
        BATCH_OUTPUT_RULES,
    ]
    return " ".join(part for part in parts if part).strip()


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
        group: str | None = None,
    ) -> str:
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

        instructions = build_instructions(lang_from, lang_to, group=group)

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
        group: str | None = None,
        chunk_size: int = 25,
    ) -> list[str]:
        if not texts or not lang_to:
            return []

        instructions = build_batch_instructions(lang_from, lang_to, group=group)

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
                        group=group,
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
