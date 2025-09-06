from typing import List

from app.models import Level, Category
from .level import LevelOutBase
from app.schemas.common import Meta, BaseSchema, ImageAssetOut


class CategoryOut(BaseSchema):
    id: int
    name: str
    current_level: LevelOutBase

    @classmethod
    def from_model(cls, category: Category, level: Level) -> "CategoryOut":
        return cls(
            id=category.id,
            name=category.name,
            current_level=LevelOutBase.model_validate(level),
        )

    class Config:
        from_attributes = True


class CategoryOutBase(BaseSchema):
    id: int
    name: str
    image: ImageAssetOut | None = None

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOutBase]
    meta: Meta
