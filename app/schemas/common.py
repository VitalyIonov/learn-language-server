from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from app.constants.common import JS_INT_MAX
from app.utils import to_camel

NonNegativeInt = Annotated[int, Field(ge=0, le=JS_INT_MAX)]
PositiveInt = Annotated[int, Field(ge=1, le=JS_INT_MAX)]


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Meta(BaseSchema):
    total_count: NonNegativeInt
