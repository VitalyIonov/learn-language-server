from app.schemas.common import BaseSchema


class CategoryProgressInfoCreate(BaseSchema):
    user_id: int
    category_id: int
    current_level_id: int


class CategoryProgressInfoUpdate(BaseSchema):
    current_level_id: int
    score: int
