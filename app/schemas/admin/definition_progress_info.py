from pydantic import Field

from app.schemas.base import BaseSchema


class DefinitionProgressInfoCreate(BaseSchema):
    user_id: int
    meaning_id: int
    definition_id: int
    level_id: int
    category_id: int


class DefinitionProgressInfoUpdate(BaseSchema):
    chance: float = Field(gt=0)
