from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import gather
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from app.models.definition import Definition
from app.models.associations import definitions_meanings
from app.schemas import DefinitionListResponse, DefinitionUpdate, DefinitionCreate
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT, MAX_LIMIT


async def get_definitions(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> DefinitionListResponse:
    offset = max(offset, 0)
    limit = min(max(limit, 1), MAX_LIMIT)

    statement = (
        select(Definition).options(
            selectinload(Definition.category),
            selectinload(Definition.level),
            selectinload(Definition.meanings),
        )
    ).order_by(Definition.text, Definition.id)
    count_statement = select(func.count()).select_from(Definition)

    if q:
        expr = Definition.text.ilike(f"%{q}%")
        statement = statement.where(expr)
        count_statement = count_statement.where(expr)

    items_task = db.execute(statement.offset(offset).limit(limit))
    count_task = db.execute(count_statement)
    items_res, count_res = await gather(items_task, count_task)

    orm_items = items_res.scalars().all()
    total = count_res.scalar_one()

    return DefinitionListResponse.model_validate(
        {"items": orm_items, "meta": {"total_count": total}}
    )


async def get_definition(db: AsyncSession, definition_id: int) -> Optional[Definition]:
    stmt = (
        select(Definition)
        .options(selectinload(Definition.meanings))
        .where(Definition.id == definition_id)
    )

    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_definition(db: AsyncSession, new_item: DefinitionCreate) -> Definition:
    payload = new_item.model_dump(exclude={"meaning_ids"})
    definition = Definition(**payload)

    if new_item.meaning_ids:
        from app.models.meaning import Meaning

        q = select(Meaning).where(Meaning.id.in_(new_item.meaning_ids))
        result = await db.scalars(q)
        definition.meanings = result.all()

    db.add(definition)
    await db.commit()
    await db.refresh(definition)
    return definition


async def update_definition(
    db: AsyncSession, db_item: Definition, item_update: DefinitionUpdate
) -> Definition:
    payload = item_update.model_dump(exclude={"meaning_ids"})

    for field, value in payload.items():
        setattr(db_item, field, value)

    if item_update.meaning_ids:
        from app.models.meaning import Meaning

        q = select(Meaning).where(Meaning.id.in_(item_update.meaning_ids))
        result = await db.scalars(q)
        db_item.meanings = result.all()

    await db.commit()
    await db.refresh(db_item)
    return db_item


async def delete_definition(db: AsyncSession, item_id: int) -> bool:
    await db.execute(
        delete(definitions_meanings).where(
            definitions_meanings.c.definition_id == item_id
        )
    )

    stmt = delete(Definition).where(Definition.id == item_id).returning(Definition.id)
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None
