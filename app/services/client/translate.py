from fastapi import HTTPException
from transformers import pipeline
from openai import OpenAI
from app.core.config import settings

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-ru")
client = OpenAI(api_key=settings.OPENAI_API_KEY)


class TranslateService:
    _translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-ru")

    @classmethod
    def translate(cls, text: str) -> str:
        if not text:
            raise HTTPException(status_code=400, detail="Missing 'text' parameter")

        result = cls._translator(text)
        return result[0]["translation_text"]
