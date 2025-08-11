from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.common import DefinitionProgressInfo
from app.schemas.admin import DefinitionProgressInfoCreate, DefinitionProgressInfoUpdate


async def get_definition_progress_info(
    db: AsyncSession, user_id: int, meaning_id: int, definition_id: int
) -> Optional[DefinitionProgressInfo]:
    result = await db.execute(
        select(DefinitionProgressInfo).where(
            DefinitionProgressInfo.user_id == user_id,
            DefinitionProgressInfo.meaning_id == meaning_id,
            DefinitionProgressInfo.definition_id == definition_id,
        )
    )
    return result.scalar_one_or_none()


async def create_definition_progress_info(
    db: AsyncSession, payload: DefinitionProgressInfoCreate
) -> DefinitionProgressInfo:
    entity = DefinitionProgressInfo(**payload.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


async def update_definition_progress_info(
    db: AsyncSession,
    db_entity: DefinitionProgressInfo,
    payload: DefinitionProgressInfoUpdate,
) -> DefinitionProgressInfo:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_entity, field, value)
        await db.commit()
        await db.refresh(db_entity)
    return db_entity
