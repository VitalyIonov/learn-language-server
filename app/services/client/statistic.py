from datetime import date, datetime

from sqlalchemy import select, case, literal, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func, coalesce

from app.constants.score import BASE_SCORE
from app.models import (
    Meaning,
    MeaningProgressInfo,
    Level,
    Definition,
    DefinitionsMeanings,
    Question,
)


class StatisticService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _get_capped_score_stmt(self):
        return case(
            (MeaningProgressInfo.score >= BASE_SCORE, literal(BASE_SCORE)),
            else_=MeaningProgressInfo.score,
        )

    def _calculate_progress_percentage(
        self, meanings_count: int, current_score: int
    ) -> float:
        if meanings_count == 0:
            return 0.0

        max_score = BASE_SCORE * meanings_count
        ratio = current_score / max_score
        percents = round(ratio * 100, 2)

        return max(0.0, min(100.0, percents))

    async def _get_current_score_by_user(self, user_id: int) -> int:
        current_score_stmt = (
            select(coalesce(func.sum(self._get_capped_score_stmt()), 0))
            .select_from(MeaningProgressInfo)
            .join(Meaning, Meaning.id == MeaningProgressInfo.meaning_id)
            .where(
                MeaningProgressInfo.user_id == user_id,
            )
        )

        return (await self.db.execute(current_score_stmt)).scalar_one()

    async def _get_current_score_by_category(
        self, user_id: int, level_id: int, category_id: int
    ) -> int:
        current_score_stmt = (
            select(coalesce(func.sum(self._get_capped_score_stmt()), 0))
            .join(Meaning, Meaning.id == MeaningProgressInfo.meaning_id)
            .where(
                MeaningProgressInfo.user_id == user_id,
                MeaningProgressInfo.level_id == level_id,
                Meaning.category_id == category_id,
            )
        )

        return (await self.db.execute(current_score_stmt)).scalar_one()

    async def _get_unique_meanings_count(self) -> int:
        meanings_count_stmt = (
            select(
                func.count(
                    distinct(
                        func.concat(
                            Definition.level_id, "-", DefinitionsMeanings.meaning_id
                        )
                    )
                )
            )
            .select_from(Definition)
            .join(
                DefinitionsMeanings, DefinitionsMeanings.definition_id == Definition.id
            )
            .where(Definition.level_id.is_not(None))
        )

        return (await self.db.execute(meanings_count_stmt)).scalar_one()

    async def get_progress_by_user(self, user_id: int) -> float:
        meanings_count = await self._get_unique_meanings_count()
        current_score = await self._get_current_score_by_user(user_id=user_id)

        result = self._calculate_progress_percentage(meanings_count, current_score)
        return result

    async def get_today_progress_by_user(self, user_id: int) -> float:
        answered_meanings_today = select(func.distinct(Question.meaning_id)).where(
            Question.user_id == user_id,
            Question.is_correct.isnot(None),
            Question.updated_at >= datetime.combine(date.today(), datetime.min.time()),
        )

        past_score_stmt = (
            select(coalesce(func.sum(self._get_capped_score_stmt()), 0))
            .select_from(MeaningProgressInfo)
            .where(
                MeaningProgressInfo.user_id == user_id,
                MeaningProgressInfo.meaning_id.not_in(answered_meanings_today),
            )
        )

        meanings_count = await self._get_unique_meanings_count()
        current_score = await self._get_current_score_by_user(user_id=user_id)
        past_score = (await self.db.execute(past_score_stmt)).scalar_one()
        today_score = current_score - past_score

        result = self._calculate_progress_percentage(meanings_count, today_score)
        return result

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

        meanings_count = (await self.db.execute(meanings_count_stmt)).scalar_one()
        current_score = await self._get_current_score_by_category(
            user_id=user_id, level_id=level_id, category_id=category_id
        )

        result = self._calculate_progress_percentage(meanings_count, current_score)
        return result
