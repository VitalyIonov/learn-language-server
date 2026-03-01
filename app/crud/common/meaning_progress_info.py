from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MeaningProgressInfo


async def get_scores_by_levels(
    db: AsyncSession, user_id: int, category_id: int, level_ids: list[int]
) -> dict[int, int]:
    statement = (
        select(
            MeaningProgressInfo.level_id,
            func.sum(MeaningProgressInfo.score).label("current_score"),
        )
        .where(
            MeaningProgressInfo.user_id == user_id,
            MeaningProgressInfo.category_id == category_id,
            MeaningProgressInfo.level_id.in_(level_ids),
        )
        .group_by(MeaningProgressInfo.level_id)
    )

    result = await db.execute(statement)
    return {row.level_id: row.current_score for row in result.all()}


async def get_scores_by_categories(
    db: AsyncSession, user_id: int, category_ids: list[int]
) -> dict[int, int]:
    statement = (
        select(
            MeaningProgressInfo.category_id,
            func.sum(MeaningProgressInfo.score).label("current_score"),
        )
        .where(
            MeaningProgressInfo.user_id == user_id,
            MeaningProgressInfo.category_id.in_(category_ids),
        )
        .group_by(MeaningProgressInfo.category_id)
    )

    result = await db.execute(statement)
    return {row.category_id: row.current_score for row in result.all()}
