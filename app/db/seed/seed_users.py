from sqlalchemy import select, insert
from app.models.common import User
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_users(session: AsyncSession, data: list[dict]):
    for user in data:
        result = await session.execute(select(User).where(User.email == user["email"]))
        if not result.scalar():
            stmt = insert(User).values(**user)
            await session.execute(stmt)
    await session.commit()
