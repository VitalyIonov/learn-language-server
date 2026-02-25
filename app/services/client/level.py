from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    get_levels as crud_get_levels,
    get_levels_base_by_ids as crud_get_levels_base_by_ids,
)
from app.crud.common import (
    get_definition_stats as crud_get_definition_stats,
    get_scores_by_levels as crud_get_scores_by_levels,
)
from app.schemas.common import DefinitionStatRow
from app.constants.definition_group import DefinitionGroup
from app.constants.score import DEFINITION_GROUP_SCORES
from app.schemas.client import LevelsListResponse, LevelScoreOut, LevelsScoreListResponse


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


def _get_level_max_scores(stats_rows: list[DefinitionStatRow]) -> dict[int, int]:
    level_group_data: dict[int, dict[DefinitionGroup, list[int]]] = defaultdict(lambda: defaultdict(list))
    for row in stats_rows:
        level_group_data[row.level_id][row.group].append(row.def_count)

    result: dict[int, int] = {}
    for level_id, groups in level_group_data.items():
        level_score = sum(_compute_group_score(group, defs_per_meaning) for group, defs_per_meaning in groups.items())
        if level_score > 0:
            result[level_id] = level_score

    return result


class LevelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int, category_id: int) -> LevelsListResponse:
        return await crud_get_levels(self.db, user_id=user_id, category_id=category_id)

    async def get_all_by_score(self, user_id: int, category_id: int) -> LevelsScoreListResponse:
        definitions_stat_rows = await crud_get_definition_stats(self.db, category_id=category_id)
        max_scores = _get_level_max_scores(definitions_stat_rows)

        if not max_scores:
            return LevelsScoreListResponse(items=[])

        level_ids = list(max_scores.keys())
        levels = await crud_get_levels_base_by_ids(self.db, level_ids=level_ids)
        current_scores = await crud_get_scores_by_levels(self.db, user_id=user_id, category_id=category_id, level_ids=level_ids)

        items = [
            LevelScoreOut(
                id=level.id,
                name=level.name,
                alias=level.alias,
                value=level.value,
                current_score=current_scores.get(level.id, 0),
                max_score=max_scores[level.id],
            )
            for level in levels
        ]

        return LevelsScoreListResponse(items=items)
