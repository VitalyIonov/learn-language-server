from collections import defaultdict
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func, coalesce

from app.constants.definition import DefinitionGroup
from app.crud.client import get_categories_by_ids as crud_get_categories_by_ids
from app.crud.common import (
    get_all_definition_stats as crud_get_all_definition_stats,
    get_scores_by_categories as crud_get_scores_by_categories,
)
from app.models import Question
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

    async def get_today_score_by_user(self, user_id: int) -> int:
        today_score_stmt = (
            select(coalesce(func.sum(Question.score_delta), 0)).where(
                Question.user_id == user_id,
                Question.updated_at
                >= datetime.combine(date.today(), datetime.min.time()),
            )
        )

        return (await self.db.execute(today_score_stmt)).scalar_one() or 0

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
