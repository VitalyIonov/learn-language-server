from typing import Optional

from app.schemas.common import BaseSchema


class TTSGenerate(BaseSchema):
    text: str


class TTSGenerateOut(BaseSchema):
    content_type: str
    data: bytes
    duration_sec: Optional[float] = None
