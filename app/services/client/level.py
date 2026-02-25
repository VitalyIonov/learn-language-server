from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_levels as crud_get_levels,
    get_levels_by_ids as crud_get_levels_by_ids,
)
from app.crud.common import get_definition_stats as crud_get_definition_stats
from app.schemas.common import DefinitionStatRow
from app.constants.definition_group import DefinitionGroup
from app.constants.score import DEFINITION_GROUP_SCORES
from app.schemas.client import LevelsListResponse


def _compute_group_score(group: DefinitionGroup, defs_per_meaning: list[int]) -> int:
    meanings_count = len(defs_per_meaning)
    score_per_def = DEFINITION_GROUP_SCORES[group]
    total_defs = sum(defs_per_meaning)

    if meanings_count <= 1:
        return 0

    if meanings_count == 2:
        min_defs = min(defs_per_meaning)
        if min_defs >= 2:
            return total_defs * score_per_def
        return min_defs * score_per_def

    return total_defs * score_per_def


def _get_available_level_ids(stats_rows: list[DefinitionStatRow]) -> list[int]:
    level_group_data: dict[int, dict[DefinitionGroup, list[int]]] = defaultdict(lambda: defaultdict(list))
    for row in stats_rows:
        level_group_data[row.level_id][row.group].append(row.def_count)

    available: list[int] = []
    for level_id, groups in level_group_data.items():
        level_score = sum(_compute_group_score(group, defs_per_meaning) for group, defs_per_meaning in groups.items())
        if level_score > 0:
            available.append(level_id)

    return available


class LevelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int, category_id: int) -> LevelsListResponse:
        return await crud_get_levels(self.db, user_id=user_id, category_id=category_id)

    async def get_all_by_score(self, user_id: int, category_id: int) -> LevelsListResponse:
        definitions_stat_rows = await crud_get_definition_stats(self.db, category_id=category_id)
        available_level_ids = _get_available_level_ids(definitions_stat_rows)

        if not available_level_ids:
            return LevelsListResponse(items=[])

        return await crud_get_levels_by_ids(self.db, user_id=user_id, category_id=category_id, level_ids=available_level_ids)
