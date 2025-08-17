from typing import List

from app.schemas.common import Meta, BaseSchema, AssetOut


class CategoryOut(BaseSchema):
    id: int
    name: str
    image: AssetOut | None = None

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOut]
    meta: Meta


class CategoryCreate(BaseSchema):
    name: str
    image_id: int | None = None

    class Config:
        from_attributes = True


class CategoryUpdate(BaseSchema):
    name: str | None = None
    image_id: int | None = None

    class Config:
        from_attributes = True
