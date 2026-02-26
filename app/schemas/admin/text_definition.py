from typing import Literal, Optional

from pydantic import ConfigDict, Field
from app.schemas.common import Meta, AudioAssetOut
from app.schemas.base import BaseSchema
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut
from app.models import QuestionTypeName
from app.constants.definition_group import TextDefinitionGroup


class TextDefinitionOut(BaseSchema):
    id: int

    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    text: str
    group: TextDefinitionGroup

    audio: Optional[AudioAssetOut] = None
    category: Optional[CategoryOut] = None
    level: Optional[LevelOut] = None
    meanings: list[MeaningOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionOutIds(BaseSchema):
    id: int
    text: str
    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    group: TextDefinitionGroup
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
    group: TextDefinitionGroup

    audio_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    meaning_ids: list[int] = Field(default_factory=list)


class TextDefinitionUpdate(BaseSchema):
    text: Optional[str] = None
    group: Optional[TextDefinitionGroup] = None

    audio_id: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    meaning_ids: Optional[list[int]] = None
