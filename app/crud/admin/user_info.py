from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.common import UserInfo
from app.schemas.admin import UserInfoCreate, UserInfoUpdate


async def get_user_info(db: AsyncSession, user_id: int) -> Optional[UserInfo]:
    result = await db.execute(select(UserInfo).where(UserInfo.user_id == user_id))
    return result.scalar_one_or_none()


async def create_user_info(db: AsyncSession, payload: UserInfoCreate) -> UserInfo:
    user_info = UserInfo(**payload.model_dump())
    db.add(user_info)
    await db.commit()
    await db.refresh(user_info)
    return user_info


async def update_user_info(
    db: AsyncSession, db_user_info: UserInfo, payload: UserInfoUpdate
) -> UserInfo:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_user_info, field, value)
        await db.commit()
        await db.refresh(db_user_info)
    return db_user_info
