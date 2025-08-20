from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.models.common import Level
from app.schemas.admin import LevelCreate, LevelsListResponse
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


async def create_level(db: AsyncSession, new_level: LevelCreate) -> Level:
    payload = new_level.model_dump(exclude={"question_type_ids"})
    level = Level(**payload)

    if new_level.question_type_ids:
        from app.models.common import QuestionType

        q = select(QuestionType).where(QuestionType.id.in_(new_level.question_type_ids))
        result = await db.scalars(q)
        level.question_types = list(result.all())

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


async def get_next_level(db: AsyncSession, level_id: int) -> Optional[Level]:
    current_value_stmt = (
        select(Level.value).where(Level.id == level_id).scalar_subquery()
    )

    level_stmt = (
        select(Level)
        .where(Level.value > current_value_stmt)
        .order_by(Level.value.asc())
        .limit(1)
    )

    next_level = (await db.execute(level_stmt)).scalar_one_or_none()

    return next_level


async def get_first_level(db: AsyncSession) -> Optional[Level]:
    level_stmt = select(Level).order_by(Level.value.asc()).limit(1)

    first_level = (await db.execute(level_stmt)).scalar_one_or_none()

    return first_level
