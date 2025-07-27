from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.models.level import Level
from app.models.meaning import Meaning


async def seed_meanings(session: AsyncSession, meanings_data: list[dict]) -> None:
    async with session.begin():
        for m in meanings_data:
            exists = await session.execute(
                select(Meaning).where(Meaning.name == m["name"])
            )
            if exists.scalars().first():
                continue

            category_id = await session.scalar(
                select(Category.id).where(Category.name == m["category"])
            )
            level_id = await session.scalar(
                select(Level.id).where(Level.alias == m["level"])
            )

            session.add(
                Meaning(
                    name=m["name"],
                    category_id=category_id,
                    level_id=level_id,
                )
            )
