from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.common import Meaning


async def get_meaning(db: AsyncSession, meaning_id: int) -> Optional[Meaning]:
    return await db.get(Meaning, meaning_id)
