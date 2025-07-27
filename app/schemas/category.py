from pydantic import Field
from typing import List
from app.schemas import Meta, NonNegativeInt, BaseSchema


class CategoryOut(BaseSchema):
    id: NonNegativeInt
    name: str

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOut] = Field(
        ..., min_length=0, max_length=100, description="Список категорий"
    )
    meta: Meta


class CategoryCreate(BaseSchema):
    name: str

    class Config:
        from_attributes = True
