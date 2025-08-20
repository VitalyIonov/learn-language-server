from typing import Union, Annotated, Literal, TypeAlias

from pydantic import ConfigDict, Field

from app.models import QuestionTypeName
from app.schemas.common import BaseSchema, AssetOut


class BaseDefinitionOut(BaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionOut(BaseDefinitionOut):
    type: Literal[QuestionTypeName.TEXT] = QuestionTypeName.TEXT
    text: str


class ImageDefinitionOut(BaseDefinitionOut):
    type: Literal[QuestionTypeName.IMAGE] = QuestionTypeName.IMAGE
    image_id: int
    image: AssetOut


DefinitionOut: TypeAlias = Annotated[
    Union[TextDefinitionOut, ImageDefinitionOut], Field(discriminator="type")
]
