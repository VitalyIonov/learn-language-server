from sqlalchemy import select

from app.models import Level
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_levels(session: AsyncSession, data: list[dict]):
    async with session.begin():
        for level_data in data:
            result = await session.execute(
                select(Level).where(Level.alias == level_data["alias"])
            )
            if result.scalars().first():
                continue

            level = Level(
                name=level_data["name"],
                alias=level_data["alias"],
                value=level_data["value"],
                language=level_data["language"],
            )

            session.add(level)
