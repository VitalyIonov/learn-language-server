import httpx
from fastapi import HTTPException
from app.core.config import settings

DEEPL_API_KEY = settings.DEEPL_API_KEY
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


class DeepLTranslateService:
    @staticmethod
    def translate(text: str, source_lang: str = "ES", target_lang: str = "RU") -> str:
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' parameter")

        headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}
        data = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
        }

        try:
            resp = httpx.post(DEEPL_API_URL, data=data, headers=headers, timeout=15)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"DeepL API error: {str(e)}")

        result = resp.json()
        return result["translations"][0]["text"]
