from typing import List

from app.constants.target_language import TargetLanguageCode
from app.schemas.base import BaseSchema


class LevelOutBase(BaseSchema):
    id: int
    name: str
    alias: str
    value: float
    language: TargetLanguageCode

    class Config:
        from_attributes = True


class LevelOut(LevelOutBase):
    current_score: int
    max_score: int
    is_active: bool


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]
