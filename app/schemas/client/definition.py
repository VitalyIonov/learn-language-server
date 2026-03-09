from typing import Union, Annotated, Literal, TypeAlias, Optional

from pydantic import ConfigDict, Field

from app.models import QuestionTypeName
from app.schemas.common import ImageAssetOut, AudioAssetOut
from app.schemas.base import BaseSchema
from app.constants.target_language import TargetLanguageCode


class BaseDefinitionOut(BaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TextDefinitionOut(BaseDefinitionOut):
    type: Literal[QuestionTypeName.TEXT]
    text: str
    language: TargetLanguageCode
    audio: Optional[AudioAssetOut] = None


class ImageDefinitionOut(BaseDefinitionOut):
    type: Literal[QuestionTypeName.IMAGE]
    text: str
    language: TargetLanguageCode
    image_id: int
    image: ImageAssetOut


DefinitionOut: TypeAlias = Annotated[
    Union[TextDefinitionOut, ImageDefinitionOut], Field(discriminator="type")
]
