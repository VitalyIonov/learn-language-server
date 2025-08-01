from pydantic import ConfigDict, Field
from app.schemas.common import BaseSchema, Meta
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut


class DefinitionOut(BaseSchema):
    id: int
    text: str
    category: CategoryOut | None = None
    level: LevelOut | None = None
    meanings: list[MeaningOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class DefinitionOutIds(BaseSchema):
    id: int
    text: str
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class DefinitionListResponse(BaseSchema):
    items: list[DefinitionOut]
    meta: Meta


class DefinitionCreate(BaseSchema):
    text: str
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)


class DefinitionUpdate(BaseSchema):
    text: str | None = None
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] | None = None
