from typing import Optional

from app.schemas.common import BaseSchema


class LevelProgressByCategoryStatistic(BaseSchema):
    progress: float
    current_level: str
    next_level: Optional[str] = None
