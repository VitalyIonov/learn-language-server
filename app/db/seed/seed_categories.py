from sqlalchemy import select, insert
from app.models.common import Category
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_categories(session: AsyncSession, data: list[dict]):
    for category in data:
        result = await session.execute(
            select(Category).where(Category.name == category["name"])
        )
        if not result.scalar():
            stmt = insert(Category).values(**category)
            await session.execute(stmt)
    await session.commit()
