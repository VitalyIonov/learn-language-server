from sqlalchemy import select

from app.models import Level
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_levels(session: AsyncSession, data: list[dict]):
    async with session.begin():
        for item in data:
            result = await session.execute(
                select(Level).where(Level.alias == item["alias"])
            )
            if result.scalars().first():
                continue

            level = Level(
                name=item["name"],
                alias=item["alias"],
                value=item["value"],
            )

            session.add(level)
