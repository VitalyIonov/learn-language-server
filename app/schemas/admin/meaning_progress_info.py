from app.constants.target_language import TargetLanguageCode
from app.schemas.base import BaseSchema


class MeaningProgressInfoCreate(BaseSchema):
    user_id: int
    meaning_id: int
    level_id: int
    category_id: int
    language: TargetLanguageCode


class MeaningProgressInfoUpdate(BaseSchema):
    score: int
