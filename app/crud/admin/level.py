from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, exists, case

from app.models import Definition
from app.models.common import Level
from app.schemas.admin import LevelCreate, LevelsListResponse
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


async def create_level(db: AsyncSession, new_level: LevelCreate) -> Level:
    level = Level(**new_level.model_dump())
    db.add(level)
    await db.commit()
    await db.refresh(level)
    return level


async def get_level(db: AsyncSession, level_id: int) -> Optional[Level]:
    return await db.get(Level, level_id)


async def get_levels(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> LevelsListResponse:
    statement = select(Level).order_by(Level.alias)
    count_statement = select(func.count()).select_from(Level)

    if q:
        statement = statement.where(Level.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(Level.name.ilike(f"%{q}%"))

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    total = (await db.execute(count_statement)).scalar_one()
    orm_items = result.scalars().all()

    return LevelsListResponse.model_validate(
        {
            "items": orm_items,
            "meta": {"total_count": total},
        }
    )


async def delete_level(db: AsyncSession, level_id: int) -> bool:
    stmt = delete(Level).where(Level.id == level_id).returning(Level.id)
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None


async def get_next_available_level(
    db: AsyncSession, category_id: int, level_id: int
) -> Optional[Level]:
    current_level_value_sq = (
        select(Level.value).where(Level.id == level_id).scalar_subquery()
    )

    defs_exists = exists().where(
        Definition.level_id == Level.id,
        Definition.category_id == category_id,
    )

    statement = (
        select(Level)
        .where(defs_exists)
        .where(Level.value > current_level_value_sq)
        .order_by(Level.value)
        .limit(1)
    )

    level = (await db.execute(statement)).scalar_one_or_none()

    return level


async def get_first_level(db: AsyncSession) -> Optional[Level]:
    level_stmt = select(Level).order_by(Level.value.asc()).limit(1)

    first_level = (await db.execute(level_stmt)).scalar_one_or_none()

    return first_level
