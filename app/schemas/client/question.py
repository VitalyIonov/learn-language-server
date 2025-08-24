from typing import Optional, Literal, Annotated, Union

from pydantic import Field, BaseModel
from app.schemas.common import BaseSchema
from .level import LevelOutBase
from .definition import DefinitionOut
from .meaning import MeaningOut
from app.models import QuestionTypeName


class LevelUpInfo(BaseModel):
    type: Literal["level_up"]
    new_level: LevelOutBase


class CategoryFinishInfo(BaseModel):
    type: Literal["category_finish"]


Info = Annotated[Union[LevelUpInfo, CategoryFinishInfo], Field(discriminator="type")]


class QuestionOut(BaseSchema):
    id: int
    type: QuestionTypeName
    meaning: MeaningOut | None = None
    definitions: list[DefinitionOut]


class QuestionGenerate(BaseSchema):
    level_id: int
    category_id: int


class QuestionCreate(BaseSchema):
    user_id: int
    meaning_id: int
    level_id: int
    category_id: int
    correct_definition_id: int
    type: QuestionTypeName


class QuestionUpdate(BaseSchema):
    chosen_definition_id: int


class QuestionUpdateOut(BaseSchema):
    is_correct: bool
    info: Optional[Info] = None
