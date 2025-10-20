from typing import Optional

from app.schemas.base import BaseSchema


class TranslationOut(BaseSchema):
    translation: str


class TranslationCreate(BaseSchema):
    text: str
    context: Optional[str] = None
    translated_text: str
    lang_from: str
    lang_to: str
