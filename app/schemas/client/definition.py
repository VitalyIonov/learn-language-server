from pydantic import ConfigDict
from app.schemas.common import BaseSchema


class DefinitionOut(BaseSchema):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)
