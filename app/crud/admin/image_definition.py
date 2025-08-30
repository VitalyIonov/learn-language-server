from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, or_, nullslast
from sqlalchemy.orm import selectinload

from app.models import Category, Level, Meaning
from app.models.common import ImageDefinition, DefinitionsMeanings
from app.schemas.admin import (
    ImageDefinitionListResponse,
    ImageDefinitionUpdate,
    ImageDefinitionCreate,
)
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT, MAX_LIMIT


async def get_image_definitions(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> ImageDefinitionListResponse:
    offset = max(offset, 0)
    limit = min(max(limit, 1), MAX_LIMIT)

    filters = []
    if q:
        expr = or_(
            ImageDefinition.category.has(Category.name.ilike(f"%{q}%")),
            ImageDefinition.level.has(Level.alias.ilike(f"%{q}%")),
            ImageDefinition.level.has(Level.name.ilike(f"%{q}%")),
            ImageDefinition.meanings.any(Meaning.name.ilike(f"%{q}%")),
        )
        filters.append(expr)

    base = (
        select(ImageDefinition)
        .options(
            selectinload(ImageDefinition.category),
            selectinload(ImageDefinition.level),
            selectinload(ImageDefinition.meanings),
        )
        .where(*filters)
    )

    items_stmt = (
        base.outerjoin(Level, ImageDefinition.level)  # LEFT JOIN levels
        .order_by(nullslast(Level.value), ImageDefinition.id)
        .offset(offset)
        .limit(limit)
    )

    count_stmt = select(func.count()).select_from(ImageDefinition).where(*filters)

    try:
        items_res = await db.execute(items_stmt)
        count_res = await db.execute(count_stmt)
    except Exception:
        await db.rollback()
        raise

    orm_items = items_res.scalars().all()
    total = count_res.scalar_one()

    return ImageDefinitionListResponse.model_validate(
        {"items": orm_items, "meta": {"total_count": total}}
    )


async def get_image_definition(
    db: AsyncSession, definition_id: int
) -> Optional[ImageDefinition]:
    return await db.get(
        ImageDefinition, definition_id, options=[selectinload(ImageDefinition.meanings)]
    )


async def create_image_definition(
    db: AsyncSession, new_item: ImageDefinitionCreate
) -> ImageDefinition:
    payload = new_item.model_dump(exclude={"meaning_ids"})
    definition = ImageDefinition(**payload)

    if new_item.meaning_ids:
        from app.models.common import Meaning

        q = select(Meaning).where(Meaning.id.in_(new_item.meaning_ids))
        result = await db.scalars(q)
        definition.meanings = list(result.all())

    db.add(definition)
    await db.commit()
    await db.refresh(definition)
    return definition


async def update_image_definition(
    db: AsyncSession, db_item: ImageDefinition, item_update: ImageDefinitionUpdate
) -> ImageDefinition:
    payload = item_update.model_dump(exclude={"meaning_ids"})

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


async def delete_image_definition(db: AsyncSession, item_id: int) -> bool:
    await db.execute(
        delete(DefinitionsMeanings).where(DefinitionsMeanings.definition_id == item_id)
    )

    stmt = (
        delete(ImageDefinition)
        .where(ImageDefinition.id == item_id)
        .returning(ImageDefinition.id)
    )
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None
