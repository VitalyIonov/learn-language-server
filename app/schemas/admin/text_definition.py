from typing import Literal

from pydantic import ConfigDict, Field
from app.schemas.common import BaseSchema, Meta
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut
from app.models import QuestionTypeName


class TextDefinitionOut(BaseSchema):
    id: int

    text: str
    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT

    category: CategoryOut | None = None
    level: LevelOut | None = None
    meanings: list[MeaningOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionOutIds(BaseSchema):
    id: int
    text: str
    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionListResponse(BaseSchema):
    items: list[TextDefinitionOut]
    meta: Meta


class TextDefinitionCreate(BaseSchema):
    text: str
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)


class TextDefinitionUpdate(BaseSchema):
    text: str | None = None
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] | None = None
