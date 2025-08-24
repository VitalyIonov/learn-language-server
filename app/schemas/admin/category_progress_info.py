from typing import Optional

from app.schemas.admin import LevelOut
from app.schemas.common import BaseSchema


class CategoryProgressInfoOut(BaseSchema):
    score: int
    level: LevelOut

    class Config:
        from_attributes = True


class CategoryProgressInfoCreate(BaseSchema):
    user_id: int
    category_id: int
    level_id: int


class CategoryProgressInfoUpdate(BaseSchema):
    score: int


class UpdateCategoryLevelResult(BaseSchema):
    new_next_cpi: Optional[CategoryProgressInfoOut] = None
    next_level: Optional[LevelOut] = None
