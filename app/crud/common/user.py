from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
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
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> UsersListResponse:
    statement = select(User).offset(offset).limit(limit)
    count_statement = select(func.count()).select_from(User)

    if q:
        statement = statement.where(User.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(User.name.ilike(f"%{q}%"))

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    total = (await db.execute(count_statement)).scalar_one()
    orm_items = result.scalars().all()

    return UsersListResponse.model_validate(
        {
            "items": orm_items,
            "meta": {"total_count": total},
        }
    )
