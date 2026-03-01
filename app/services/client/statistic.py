from collections import defaultdict
from datetime import date, datetime

from sqlalchemy import select, case, literal, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func, coalesce

from app.constants.definition import DefinitionGroup
from app.constants.score import BASE_SCORE
from app.crud.client import get_categories_by_ids as crud_get_categories_by_ids
from app.crud.common import (
    get_all_definition_stats as crud_get_all_definition_stats,
    get_scores_by_categories as crud_get_scores_by_categories,
)
from app.models import (
    MeaningProgressInfo,
    Definition,
    DefinitionsMeanings,
    Question,
)
from app.schemas.client import CategoriesProgressListResponse, CategoryProgressOut
from app.schemas.common import CategoryDefinitionStatRow
from app.services.client.level import compute_group_score


def _get_category_max_scores(
    stat_rows: list[CategoryDefinitionStatRow],
) -> dict[int, int]:
    category_level_group_data: dict[
        int, dict[int, dict[DefinitionGroup, list[int]]]
    ] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for row in stat_rows:
        category_level_group_data[row.category_id][row.level_id][row.group].append(
            row.def_count
        )

    result: dict[int, int] = {}
    for category_id, levels in category_level_group_data.items():
        category_score = 0
        for level_id, groups in levels.items():
            category_score += sum(
                compute_group_score(group=group, defs_per_meaning=defs_per_meaning)
                for group, defs_per_meaning in groups.items()
            )
        if category_score > 0:
            result[category_id] = category_score

    return result


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
            .where(
                MeaningProgressInfo.user_id == user_id,
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

    async def get_progress_by_categories(
        self, user_id: int
    ) -> CategoriesProgressListResponse:
        stat_rows = await crud_get_all_definition_stats(self.db)
        max_scores = _get_category_max_scores(stat_rows)

        if not max_scores:
            return CategoriesProgressListResponse(items=[])

        category_ids = list(max_scores.keys())
        categories = await crud_get_categories_by_ids(
            self.db, category_ids=category_ids
        )
        current_scores = await crud_get_scores_by_categories(
            self.db, user_id=user_id, category_ids=category_ids
        )

        items = [
            CategoryProgressOut(
                id=category.id,
                name=category.name,
                current_score=current_scores.get(category.id, 0),
                max_score=max_scores[category.id],
            )
            for category in categories
        ]

        return CategoriesProgressListResponse(items=items)
