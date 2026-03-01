from sqlalchemy import select, insert
from app.models.common import User, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_users(session: AsyncSession, data: list[dict]):
    for item in data:
        result = await session.execute(
            select(User.id).where(User.email == item["email"])
        )
        user_id = result.scalar()

        if user_id is None:
            result = await session.execute(
                insert(User).values(**item).returning(User.id)
            )
            user_id = result.scalar_one()
            await session.execute(insert(UserInfo).values(user_id=user_id))
