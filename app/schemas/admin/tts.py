from typing import Optional

from app.schemas.base import BaseSchema


class TTSGenerate(BaseSchema):
    text: str


class TTSGenerateOut(BaseSchema):
    content_type: str
    data: bytes
    duration_sec: Optional[float] = None
