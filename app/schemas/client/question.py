from pydantic import Field
from app.schemas.common import BaseSchema
from .definition import DefinitionOut
from .meaning import MeaningOut


class QuestionOut(BaseSchema):
    id: int
    meaning: MeaningOut | None = None
    definitions: list[DefinitionOut] = Field(default_factory=list)


class QuestionGenerate(BaseSchema):
    level_id: int
    category_id: int


class QuestionCreate(BaseSchema):
    user_id: int
    meaning_id: int
    level_id: int
    category_id: int
    correct_definition_id: int


class QuestionUpdate(BaseSchema):
    chosen_definition_id: int


class QuestionUpdateOut(BaseSchema):
    is_correct: bool
