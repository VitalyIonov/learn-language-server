from typing import List

from app.constants.target_language import TargetLanguageCode
from app.schemas.common import Meta, ImageAssetOut
from app.schemas.base import BaseSchema


class CategoryOut(BaseSchema):
    id: int
    name: str
    language: TargetLanguageCode

    class Config:
        from_attributes = True


class CategoryOutBase(BaseSchema):
    id: int
    name: str
    language: TargetLanguageCode
    image: ImageAssetOut | None = None
    current_score: int
    max_score: int

    class Config:
        from_attributes = True


class CategoriesListResponse(BaseSchema):
    items: List[CategoryOutBase]
    meta: Meta
