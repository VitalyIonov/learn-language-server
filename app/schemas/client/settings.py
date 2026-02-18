from typing import Optional, Literal

from app.constants.target_language import TargetLanguageCode
from app.schemas.base import BaseSchema

AllowedLang = Literal["en", "ru", "es", "fr", "it"]


class SettingsUpdate(BaseSchema):
    interface_lang: Optional[str] = None
    target_language: Optional[TargetLanguageCode] = None


class SettingsInterfaceLangUpdate(SettingsUpdate):
    interface_lang: AllowedLang


class SettingsTargetLanguageUpdate(SettingsUpdate):
    target_language: TargetLanguageCode
