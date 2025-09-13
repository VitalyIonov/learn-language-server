from pydantic import ConfigDict, Field
from typing import List, Optional
from app.schemas.common import BaseSchema, Meta
from .category import CategoryOut
from .level import LevelOut


class MeaningOut(BaseSchema):
    id: int
    name: str
    category: Optional[CategoryOut] = None
    level: Optional[LevelOut] = None

    model_config = ConfigDict(from_attributes=True)


class MeaningsListResponse(BaseSchema):
    items: List[MeaningOut] = Field(
        ..., min_length=0, max_length=100, description="Список категорий"
    )
    meta: Meta


class MeaningCreate(BaseSchema):
    name: str
    category_id: Optional[int] = None
    level_id: Optional[int] = None


class MeaningUpdate(BaseSchema):
    name: Optional[int] = None
    category_id: Optional[int] = None
    level_id: Optional[int] = None
    audio_id: Optional[int] = None
