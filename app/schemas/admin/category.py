from typing import List
from app.schemas.common import Meta, BaseSchema


class CategoryOut(BaseSchema):
    id: int
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
