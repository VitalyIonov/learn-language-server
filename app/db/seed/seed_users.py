from sqlalchemy import select, insert
from app.models.common import User, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_users(session: AsyncSession, data: list[dict]):
    for user in data:
        result = await session.execute(select(User).where(User.email == user["email"]))
        if not result.scalar():
            stmt = insert(User).values(**user).returning(User.id)
            result = await session.execute(stmt)
            user_id = result.scalar_one()

            user_info_stmt = insert(UserInfo).values(user_id=user_id)
            await session.execute(user_info_stmt)
    await session.commit()
