from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Level


async def get_levels_base_by_ids(db: AsyncSession, level_ids: list[int]) -> list[Level]:
    statement = select(Level).where(Level.id.in_(level_ids)).order_by(Level.alias)

    result = await db.execute(statement)
    return list(result.scalars().all())
