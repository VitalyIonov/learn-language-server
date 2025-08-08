from pydantic import Field
from app.schemas.common import BaseSchema
from .definition import DefinitionOut
from .meaning import MeaningOut


class QuestionOut(BaseSchema):
    meaning: MeaningOut | None = None
    definitions: list[DefinitionOut] = Field(default_factory=list)
