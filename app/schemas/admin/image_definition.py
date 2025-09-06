from typing import Literal

from pydantic import ConfigDict, Field
from app.schemas.common import BaseSchema, Meta, ImageAssetOut
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut
from app.models import QuestionTypeName


class ImageDefinitionOut(BaseSchema):
    id: int

    type: Literal[QuestionTypeName.IMAGE] = QuestionTypeName.IMAGE
    image_id: int
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)

    image: ImageAssetOut
    category: CategoryOut | None = None
    level: LevelOut | None = None
    meanings: list[MeaningOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ImageDefinitionOutIds(BaseSchema):
    id: int
    image_id: int
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ImageDefinitionListResponse(BaseSchema):
    items: list[ImageDefinitionOut]
    meta: Meta


class ImageDefinitionCreate(BaseSchema):
    image_id: int
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)


class ImageDefinitionUpdate(BaseSchema):
    image_id: int | None = None
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] | None = None
