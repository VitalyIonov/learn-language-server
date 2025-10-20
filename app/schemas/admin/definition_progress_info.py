from app.schemas.base import BaseSchema


class DefinitionProgressInfoCreate(BaseSchema):
    user_id: int
    meaning_id: int
    definition_id: int


class DefinitionProgressInfoUpdate(BaseSchema):
    score: int
