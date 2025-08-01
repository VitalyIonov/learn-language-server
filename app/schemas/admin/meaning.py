from pydantic import ConfigDict, Field
from typing import List
from app.schemas.common import BaseSchema, Meta
from .category import CategoryOut
from .level import LevelOut


class MeaningOut(BaseSchema):
    id: int
    name: str
    category: CategoryOut | None = None
    level: LevelOut | None = None

    model_config = ConfigDict(from_attributes=True)


class MeaningsListResponse(BaseSchema):
    items: List[MeaningOut] = Field(
        ..., min_length=0, max_length=100, description="Список категорий"
    )
    meta: Meta


class MeaningCreate(BaseSchema):
    name: str
    category_id: int | None = None
    level_id: int | None = None


class MeaningUpdate(BaseSchema):
    name: str | None = None
    category_id: int | None = None
    level_id: int | None = None
