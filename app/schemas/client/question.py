from typing import Optional, Literal, Annotated, Union

from pydantic import Field, BaseModel
from app.schemas.common import BaseSchema
from .definition import DefinitionOut
from .meaning import MeaningOut


class LevelUpInfo(BaseModel):
    type: Literal["level_up"]
    new_level: str


Info = Annotated[Union[LevelUpInfo], Field(discriminator="type")]


class QuestionOut(BaseSchema):
    id: int
    meaning: MeaningOut | None = None
    definitions: list[DefinitionOut] = Field(default_factory=list)


class QuestionGenerate(BaseSchema):
    level_id: Optional[int] = None
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
    info: Optional[Info] = None
