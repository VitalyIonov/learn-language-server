from typing import Optional, Literal

from app.schemas.base import BaseSchema

AllowedLang = Literal["en", "ru", "es", "fr", "it"]


class SettingsUpdate(BaseSchema):
    interface_lang: Optional[str] = None


class SettingsInterfaceLangUpdate(SettingsUpdate):
    interface_lang: AllowedLang
