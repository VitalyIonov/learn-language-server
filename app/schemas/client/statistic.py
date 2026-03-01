from typing import List

from app.schemas.base import BaseSchema


class TodayScoreStatistic(BaseSchema):
    today_score: int


class CategoryProgressOut(BaseSchema):
    id: int
    name: str
    current_score: int
    max_score: int

    class Config:
        from_attributes = True


class CategoriesProgressListResponse(BaseSchema):
    items: List[CategoryProgressOut]
