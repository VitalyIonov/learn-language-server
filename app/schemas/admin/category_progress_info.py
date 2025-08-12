from app.schemas.common import BaseSchema


class CategoryProgressInfoCreate(BaseSchema):
    user_id: int
    category_id: int
    level_id: int


class CategoryProgressInfoUpdate(BaseSchema):
    score: int
