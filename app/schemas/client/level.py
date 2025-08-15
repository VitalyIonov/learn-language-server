from typing import List, Optional, Literal, TypeVar

from pydantic import Field

from app.schemas.common import BaseSchema


class LevelOutBase(BaseSchema):
    id: int
    name: str
    alias: str
    value: int

    class Config:
        from_attributes = True


class LevelOut(LevelOutBase):
    is_locked: Optional[bool] = Field(default=None)


class LevelsListResponse(BaseSchema):
    items: List[LevelOut]
