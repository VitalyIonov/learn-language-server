from typing import Optional

from pydantic import ConfigDict
from app.schemas.common import AudioAssetOut
from app.schemas.base import BaseSchema
from app.constants.target_language import TargetLanguageCode


class MeaningOut(BaseSchema):
    id: int
    name: str
    language: TargetLanguageCode

    audio: Optional[AudioAssetOut] = None

    model_config = ConfigDict(from_attributes=True)
