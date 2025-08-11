from app.schemas.common import BaseSchema


class MeaningProgressInfoCreate(BaseSchema):
    user_id: int
    meaning_id: int
    level_id: int


class MeaningProgressInfoUpdate(BaseSchema):
    score: int
