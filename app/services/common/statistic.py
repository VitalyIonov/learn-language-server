from sqlalchemy import select, case, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func, coalesce

from app.models import Meaning, MeaningProgressInfo, Level

BASE_SCORE = 6


class StatisticService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_level_progress_by_category(
        self, user_id: int, level_id: int, category_id: int
    ) -> float:
        level_value_stmt = (
            select(Level.value).where(Level.id == level_id).scalar_subquery()
        )

        meanings_count_stmt = (
            select(func.count(Meaning.id))
            .join(Level, Level.id == Meaning.level_id)
            .where(
                Level.value <= level_value_stmt,
                Meaning.category_id == category_id,
            )
        )

        capped_score_stmt = case(
            (MeaningProgressInfo.score >= BASE_SCORE, literal(BASE_SCORE)),
            else_=MeaningProgressInfo.score,
        )

        current_score_stmt = (
            select(coalesce(func.sum(capped_score_stmt), 0))
            .join(Meaning, Meaning.id == MeaningProgressInfo.meaning_id)
            .where(
                MeaningProgressInfo.user_id == user_id,
                MeaningProgressInfo.level_id == level_id,
                Meaning.category_id == category_id,
            )
        )

        meanings_count = (await self.db.execute(meanings_count_stmt)).scalar_one()
        current_score = (await self.db.execute(current_score_stmt)).scalar_one()

        max_score = BASE_SCORE * meanings_count
        ratio = current_score / max_score
        percents = round(ratio * 100, 2)

        return max(0, min(100, percents))
