from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.common import MeaningProgressInfo
from app.schemas.admin import MeaningProgressInfoCreate, MeaningProgressInfoUpdate


async def get_meaning_progress_info(
    db: AsyncSession, user_id: int, meaning_id: int, level_id: int
) -> Optional[MeaningProgressInfo]:
    result = await db.execute(
        select(MeaningProgressInfo).where(
            MeaningProgressInfo.user_id == user_id,
            MeaningProgressInfo.meaning_id == meaning_id,
            MeaningProgressInfo.level_id == level_id,
        )
    )
    return result.scalar_one_or_none()


async def create_meaning_progress_info(
    db: AsyncSession, payload: MeaningProgressInfoCreate
) -> MeaningProgressInfo:
    entity = MeaningProgressInfo(**payload.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


async def update_meaning_progress_info(
    db: AsyncSession,
    db_entity: MeaningProgressInfo,
    payload: MeaningProgressInfoUpdate,
) -> MeaningProgressInfo:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_entity, field, value)
        await db.commit()
        await db.refresh(db_entity)
    return db_entity
