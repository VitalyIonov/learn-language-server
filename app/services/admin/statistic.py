from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func, coalesce

from app.models import Meaning, MeaningProgressInfo

BASE_SCORE = 6


class StatisticService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_level_progress_by_category(
        self, user_id: int, level_id: int, category_id: int
    ) -> int:
        meanings_count_stmt = select(func.count(Meaning.id)).where(
            Meaning.level_id == level_id, Meaning.category_id == category_id
        )
        current_score_stmt = select(
            coalesce(func.sum(MeaningProgressInfo.score), 0)
        ).where(
            MeaningProgressInfo.user_id == user_id,
            MeaningProgressInfo.level_id == level_id,
        )

        meanings_count = (await self.db.execute(meanings_count_stmt)).scalar()
        current_score = (await self.db.execute(current_score_stmt)).scalar()

        return (
            (current_score / meanings_count * BASE_SCORE) * 100 if meanings_count else 0
        )
