from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.common import User
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.schemas.common import UsersListResponse, UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, new_item: UserCreate) -> User:
    payload = new_item.model_dump()
    user = User(**payload)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_users(
    db: AsyncSession, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
) -> UsersListResponse:
    result = await db.execute(select(User).offset(offset).limit(limit))

    return UsersListResponse.model_validate({"items": result})
