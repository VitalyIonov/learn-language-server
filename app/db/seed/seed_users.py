from sqlalchemy import select, insert
from app.models.common import User, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.admin import LevelService, CategoryProgressInfoService


async def seed_users(session: AsyncSession, data: list[dict]):
    svc_level = LevelService(session)
    svc_cpi = CategoryProgressInfoService(session, svc_level)

    async with session.begin():
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

            await svc_cpi.bootstrap(user_id)
