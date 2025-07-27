from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.level import Level
from app.schemas import LevelCreate
from collections.abc import Sequence
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


async def create_level(db: AsyncSession, new_level: LevelCreate) -> Level:
    level = Level(**new_level.model_dump())
    db.add(level)
    await db.commit()
    await db.refresh(level)
    return level


async def get_levels(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> Sequence[Level]:
    statement = select(Level).order_by(Level.alias)
    count_statement = select(func.count()).select_from(Level)

    if q:
        statement = statement.where(Level.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(Level.name.ilike(f"%{q}%"))

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    count = await db.execute(count_statement)

    return {
        "items": result.scalars().all(),
        "meta": {"totalCount": count.scalar_one()},
    }
