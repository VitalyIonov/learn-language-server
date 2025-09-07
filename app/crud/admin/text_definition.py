from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import gather
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload
from app.models.common import TextDefinition, DefinitionsMeanings
from app.schemas.admin import (
    TextDefinitionListResponse,
    TextDefinitionUpdate,
    TextDefinitionCreate,
)
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT, MAX_LIMIT


async def get_text_definitions(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> TextDefinitionListResponse:
    offset = max(offset, 0)
    limit = min(max(limit, 1), MAX_LIMIT)

    statement = (
        select(TextDefinition).options(
            selectinload(TextDefinition.category),
            selectinload(TextDefinition.level),
            selectinload(TextDefinition.meanings),
        )
    ).order_by(TextDefinition.text, TextDefinition.id)
    count_statement = select(func.count()).select_from(TextDefinition)

    if q:
        expr = TextDefinition.text.ilike(f"%{q}%")
        statement = statement.where(expr)
        count_statement = count_statement.where(expr)

    items_task = db.execute(statement.offset(offset).limit(limit))
    count_task = db.execute(count_statement)
    items_res, count_res = await gather(items_task, count_task)

    orm_items = items_res.scalars().all()
    total = count_res.scalar_one()

    return TextDefinitionListResponse.model_validate(
        {"items": orm_items, "meta": {"total_count": total}}
    )


async def get_text_definition(
    db: AsyncSession, definition_id: int
) -> Optional[TextDefinition]:
    return await db.get(
        TextDefinition, definition_id, options=[selectinload(TextDefinition.meanings)]
    )


async def create_text_definition(
    db: AsyncSession, new_item: TextDefinitionCreate
) -> TextDefinition:
    payload = new_item.model_dump(exclude={"meaning_ids"})
    definition = TextDefinition(**payload)

    if new_item.meaning_ids:
        from app.models.common import Meaning

        q = select(Meaning).where(Meaning.id.in_(new_item.meaning_ids))
        result = await db.scalars(q)
        definition.meanings = list(result.all())

    db.add(definition)
    await db.commit()
    await db.refresh(definition)
    return definition


async def update_text_definition(
    db: AsyncSession, db_item: TextDefinition, item_update: TextDefinitionUpdate
) -> TextDefinition:
    payload = item_update.model_dump(exclude={"meaning_ids"}, exclude_unset=True)

    for field, value in payload.items():
        setattr(db_item, field, value)

    if item_update.meaning_ids:
        from app.models.common import Meaning

        q = select(Meaning).where(Meaning.id.in_(item_update.meaning_ids))
        result = await db.scalars(q)
        db_item.meanings = list(result.all())

    await db.commit()
    await db.refresh(db_item)
    return db_item


async def delete_text_definition(db: AsyncSession, item_id: int) -> bool:
    await db.execute(
        delete(DefinitionsMeanings).where(DefinitionsMeanings.definition_id == item_id)
    )

    stmt = (
        delete(TextDefinition)
        .where(TextDefinition.id == item_id)
        .returning(TextDefinition.id)
    )
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None
