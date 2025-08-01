from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.crud.common import (
    get_user_by_email as crud_get_user_by_email,
    get_users as crud_get_users,
)
from app.models.common import User
from app.schemas.common import UsersListResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User:
        user = await crud_get_user_by_email(self.db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def get_all(self) -> UsersListResponse:
        return await crud_get_users(self.db)

    async def require_admin(self, user: User) -> None:
        if user.role != user.role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required",
            )
