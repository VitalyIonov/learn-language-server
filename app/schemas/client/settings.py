from typing import Optional

from app.constants.interface_language import InterfaceLanguageCode
from app.constants.target_language import TargetLanguageCode
from app.schemas.base import BaseSchema


class SettingsUpdate(BaseSchema):
    interface_lang: Optional[InterfaceLanguageCode] = None
    target_language: Optional[TargetLanguageCode] = None


class SettingsInterfaceLangUpdate(SettingsUpdate):
    interface_lang: InterfaceLanguageCode


class SettingsTargetLanguageUpdate(SettingsUpdate):
    target_language: TargetLanguageCode
