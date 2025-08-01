from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from app.models.common import Meaning
from app.schemas.admin import MeaningCreate, MeaningUpdate, MeaningsListResponse
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


async def get_meanings(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> MeaningsListResponse:
    statement = (
        select(Meaning)
        .options(
            selectinload(Meaning.category),
            selectinload(Meaning.level),
        )
        .order_by(Meaning.id)
    )
    count_statement = select(func.count()).select_from(Meaning)

    if q:
        statement = statement.where(Meaning.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(Meaning.name.ilike(f"%{q}%"))

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    total = (await db.execute(count_statement)).scalar_one()
    orm_items = result.scalars().all()

    return MeaningsListResponse.model_validate(
        {"items": orm_items, "meta": {"total_count": total}}
    )


async def get_meaning(db: AsyncSession, meaning_id: int) -> Optional[Meaning]:
    return await db.get(Meaning, meaning_id)


async def create_meaning(db: AsyncSession, new_meaning: MeaningCreate) -> Meaning:
    meaning = Meaning(**new_meaning.model_dump())
    db.add(meaning)
    await db.commit()
    await db.refresh(meaning)
    return meaning


async def update_meaning(
    db: AsyncSession, db_meaning: Meaning, meaning_update: MeaningUpdate
) -> Meaning:
    update_data = meaning_update.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_meaning, field, value)
        await db.commit()
        await db.refresh(db_meaning)
    return db_meaning


async def delete_meaning(db: AsyncSession, meaning_id: int) -> bool:
    stmt = delete(Meaning).where(Meaning.id == meaning_id).returning(Meaning.id)
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None
