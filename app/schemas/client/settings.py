from typing import Optional, Literal

from app.schemas.base import BaseSchema

AllowedLang = Literal["en", "ru", "es", "fr", "it"]


class SettingsUpdate(BaseSchema):
    lang: Optional[str] = None


class SettingsLangUpdate(SettingsUpdate):
    lang: AllowedLang
