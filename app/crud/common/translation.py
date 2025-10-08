from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.common import Translation
from app.schemas.common import TranslationCreate


async def get_translation(
    db: AsyncSession, text: str, lang_from: str, lang_to: str, context: str | None
) -> Optional[Translation]:
    result = await db.execute(
        select(Translation).where(
            Translation.text == text,
            Translation.lang_from == lang_from,
            Translation.lang_to == lang_to,
            Translation.context == context,
        )
    )

    return result.scalar_one_or_none()


async def create_translation(
    db: AsyncSession, payload: TranslationCreate
) -> Translation:
    entity = Translation(**payload.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity
