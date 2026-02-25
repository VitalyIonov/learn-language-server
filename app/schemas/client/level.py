from typing import List, Optional

from pydantic import Field

from app.schemas.base import BaseSchema


class LevelOutBase(BaseSchema):
    id: int
    name: str
    alias: str
    value: float

    class Config:
        from_attributes = True


class LevelOut(LevelOutBase):
    is_locked: Optional[bool] = Field(default=None)


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]


class LevelScoreOut(LevelOutBase):
    current_score: int
    max_score: int


class LevelsScoreListResponse(BaseSchema):
    items: List[LevelScoreOut]
