from pydantic import Field
from typing import List
from app.schemas.common import BaseSchema, Meta


class QuestionCreate(BaseSchema):
    user_id: int
    meaning_id: int
    category_id: int
    definition_ids: List[int] = Field(default_factory=list)


class QuestionUpdate(BaseSchema):
    is_correct: bool
