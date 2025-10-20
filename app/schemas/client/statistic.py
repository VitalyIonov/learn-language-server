from typing import Optional

from app.schemas.base import BaseSchema


class LevelProgressByCategoryStatistic(BaseSchema):
    progress: float
    current_level: str
    next_level: Optional[str] = None


class ProgressByUserStatistic(BaseSchema):
    progress: float
