from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models import Level, CategoryProgressInfo
from app.schemas.admin import CategoryProgressInfoCreate, CategoryProgressInfoUpdate


async def get_top_category_progress_info(
    db: AsyncSession, user_id: int, category_id: int
) -> Optional[CategoryProgressInfo]:
    cpi_max_level_stmt = (
        select(CategoryProgressInfo)
        .join(CategoryProgressInfo.level)
        .where(
            CategoryProgressInfo.user_id == user_id,
            CategoryProgressInfo.category_id == category_id,
        )
        .order_by(Level.value.desc())
        .limit(1)
    )

    cpi_max_level = (await db.execute(cpi_max_level_stmt)).scalar_one_or_none()

    return cpi_max_level


async def get_category_progress_info(
    db: AsyncSession, user_id: int, category_id: int, level_id: int
) -> Optional[CategoryProgressInfo]:
    result = await db.execute(
        select(CategoryProgressInfo).where(
            CategoryProgressInfo.user_id == user_id,
            CategoryProgressInfo.category_id == category_id,
            CategoryProgressInfo.level_id == level_id,
        )
    )
    return result.scalar_one_or_none()


async def create_category_progress_info(
    db: AsyncSession, payload: CategoryProgressInfoCreate
) -> CategoryProgressInfo:
    entity = CategoryProgressInfo(**payload.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


async def update_category_progress_info(
    db: AsyncSession,
    db_entity: CategoryProgressInfo,
    payload: CategoryProgressInfoUpdate,
) -> CategoryProgressInfo:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_entity, field, value)
        await db.commit()
        await db.refresh(db_entity)
    return db_entity
