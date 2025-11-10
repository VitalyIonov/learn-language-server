from typing import Optional

from app.schemas.base import BaseSchema


class SettingsUpdate(BaseSchema):
    lang: Optional[str] = None


class SettingsLangUpdate(SettingsUpdate):
    lang: str
