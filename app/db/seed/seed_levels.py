from sqlalchemy import select, insert
from app.models.common import Level
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_levels(session: AsyncSession, data: list[dict]):
    for level in data:
        result = await session.execute(select(Level).where(Level.name == level["name"]))
        if not result.scalar():
            stmt = insert(Level).values(**level)
            await session.execute(stmt)
    await session.commit()
