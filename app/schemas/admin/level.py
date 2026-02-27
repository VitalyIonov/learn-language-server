from typing import List

from app.schemas.common import Meta
from app.schemas.base import BaseSchema


class LevelOut(BaseSchema):
    id: int
    name: str
    alias: str
    value: float

    class Config:
        from_attributes = True


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]
    meta: Meta


class LevelCreate(BaseSchema):
    name: str
    alias: str

    class Config:
        from_attributes = True
