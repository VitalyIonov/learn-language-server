from pydantic import Field
from typing import List
from app.schemas import Meta, NonNegativeInt, BaseSchema


class LevelOut(BaseSchema):
    id: NonNegativeInt
    name: str
    alias: str

    class Config:
        from_attributes = True


class LevelsListResponse(BaseSchema):
    items: List[LevelOut] = Field(
        ..., min_length=0, max_length=100, description="Список категорий"
    )
    meta: Meta


class LevelCreate(BaseSchema):
    name: str
    alias: str

    class Config:
        from_attributes = True
