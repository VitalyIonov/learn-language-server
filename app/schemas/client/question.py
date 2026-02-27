from typing import Optional, Literal, Annotated, Union, NamedTuple

from pydantic import Field, BaseModel
from app.schemas.base import BaseSchema
from .level import LevelOutBase
from .definition import DefinitionOut
from .meaning import MeaningOut
from app.models import QuestionTypeName
from app.constants.definition_group import DefinitionGroup


class LevelUpInfo(BaseModel):
    type: Literal["level_up"]
    new_level: LevelOutBase


class CategoryFinishInfo(BaseModel):
    type: Literal["category_finish"]


Info = Annotated[Union[LevelUpInfo, CategoryFinishInfo], Field(discriminator="type")]


class DefinitionCandidate(NamedTuple):
    definition_id: int
    meaning_id: int
    group: DefinitionGroup
    chance: float


class QuestionOut(BaseSchema):
    id: int
    type: QuestionTypeName
    meaning: MeaningOut
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
