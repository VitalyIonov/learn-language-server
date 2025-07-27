from typing import List
from app.schemas import Meta, NonNegativeInt, BaseSchema


class CategoryOut(BaseSchema):
    id: NonNegativeInt
    name: str

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOut]
    meta: Meta


class CategoryCreate(BaseSchema):
    name: str

    class Config:
        from_attributes = True
