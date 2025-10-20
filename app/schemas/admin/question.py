from pydantic import Field
from typing import List

from app.models import QuestionTypeName
from app.schemas.admin import CategoryOut, LevelOut
from app.schemas.base import BaseSchema


class QuestionOut(BaseSchema):
    type: QuestionTypeName
    category: CategoryOut
    level: LevelOut


class QuestionCreate(BaseSchema):
    user_id: int
    meaning_id: int
    category_id: int
    definition_ids: List[int] = Field(default_factory=list)


class QuestionUpdate(BaseSchema):
    is_correct: bool
