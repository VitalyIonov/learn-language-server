from typing import Literal, Optional

from pydantic import ConfigDict, Field
from app.schemas.common import ImageAssetOut, Meta
from app.schemas.base import BaseSchema
from .meaning import MeaningOut
from .category import CategoryOut
from .level import LevelOut
from app.models import QuestionTypeName
from app.constants.definition import ImageDefinitionGroup


class ImageDefinitionOut(BaseSchema):
    id: int

    type: Literal[QuestionTypeName.IMAGE] = QuestionTypeName.IMAGE
    image_id: int
    group: ImageDefinitionGroup
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
    group: ImageDefinitionGroup
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ImageDefinitionListResponse(BaseSchema):
    items: list[ImageDefinitionOut]
    meta: Meta


class ImageDefinitionCreate(BaseSchema):
    image_id: int
    group: ImageDefinitionGroup
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] = Field(default_factory=list)


class ImageDefinitionUpdate(BaseSchema):
    image_id: int | None = None
    group: Optional[ImageDefinitionGroup] = None
    category_id: int | None = None
    level_id: int | None = None
    meaning_ids: list[int] | None = None
