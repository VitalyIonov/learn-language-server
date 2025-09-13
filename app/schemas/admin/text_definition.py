from typing import Literal, Optional

from pydantic import ConfigDict, Field
from app.schemas.common import BaseSchema, Meta, AudioAssetOut
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut
from app.models import QuestionTypeName


class TextDefinitionOut(BaseSchema):
    id: int

    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    text: str

    audio: Optional[AudioAssetOut] = None
    category: Optional[CategoryOut] = None
    level: Optional[LevelOut] = None
    meanings: list[MeaningOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionOutIds(BaseSchema):
    id: int
    text: str
    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    audio_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    meaning_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionListResponse(BaseSchema):
    items: list[TextDefinitionOut]
    meta: Meta


class TextDefinitionCreate(BaseSchema):
    text: str

    audio_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    meaning_ids: list[int] = Field(default_factory=list)


class TextDefinitionUpdate(BaseSchema):
    text: Optional[str] = None

    audio_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    meaning_ids: Optional[list[int]] = None
