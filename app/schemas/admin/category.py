from typing import List

from app.constants.target_language import TargetLanguageCode
from app.schemas.common import ImageAssetOut, Meta
from app.schemas.base import BaseSchema


class CategoryOut(BaseSchema):
    id: int
    name: str
    language: TargetLanguageCode
    image: ImageAssetOut | None = None

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOut]
    meta: Meta


class CategoryCreate(BaseSchema):
    name: str
    language: TargetLanguageCode = TargetLanguageCode.EN
    image_id: int | None = None

    class Config:
        from_attributes = True


class CategoryUpdate(BaseSchema):
    name: str | None = None
    language: TargetLanguageCode | None = None
    image_id: int | None = None

    class Config:
        from_attributes = True
