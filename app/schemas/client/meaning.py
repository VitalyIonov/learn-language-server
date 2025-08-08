from pydantic import ConfigDict
from app.schemas.common import BaseSchema


class MeaningOut(BaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
