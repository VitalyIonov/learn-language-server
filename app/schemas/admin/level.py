from typing import List

from app.schemas.common import Meta, BaseSchema
from .question_type import QuestionTypeOut


class LevelOut(BaseSchema):
    id: int
    name: str
    alias: str
    value: float
    question_types: list[QuestionTypeOut]

    class Config:
        from_attributes = True


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]
    meta: Meta


class LevelCreate(BaseSchema):
    name: str
    alias: str
    question_type_ids: list[int]

    class Config:
        from_attributes = True
