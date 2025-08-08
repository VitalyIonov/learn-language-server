from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.common import CategoryProgressInfo
from app.schemas.admin import CategoryProgressInfoCreate, CategoryProgressInfoUpdate


async def get_category_progress_info(
    db: AsyncSession, user_id: int, category_id: int
) -> Optional[CategoryProgressInfo]:
    result = await db.execute(
        select(CategoryProgressInfo).where(
            CategoryProgressInfo.user_id == user_id,
            CategoryProgressInfo.category_id == category_id,
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
