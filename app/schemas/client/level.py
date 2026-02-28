from typing import List

from app.schemas.base import BaseSchema


class LevelOutBase(BaseSchema):
    id: int
    name: str
    alias: str
    value: float

    class Config:
        from_attributes = True


class LevelOut(LevelOutBase):
    current_score: int
    max_score: int
    is_active: bool


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]
