from typing import List

from app.schemas.common import Meta, ImageAssetOut
from app.schemas.base import BaseSchema


class CategoryOut(BaseSchema):
    id: int
    name: str

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
