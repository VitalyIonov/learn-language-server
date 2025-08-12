from typing import List

from app.models import Level, Category
from app.schemas.common import Meta, BaseSchema


class CategoryOut(BaseSchema):
    id: int
    name: str
    current_level: str

    @classmethod
    def from_model(cls, category: Category, level: Level) -> "CategoryOut":
        return cls(
            id=category.id,
            name=category.name,
            current_level=level.alias,
        )


class CategoryOutBase(BaseSchema):
    id: int
    name: str

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOutBase]
    meta: Meta
