from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.crud.common import (
    get_user_by_email as crud_get_user_by_email,
    get_users as crud_get_users,
    create_user as crud_create_user,
)
from app.models.common import User
from app.schemas.common import UsersListResponse, UserCreate
from app.schemas.admin import UserInfoCreate
from app.services.admin import UserInfoService


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        return await crud_get_user_by_email(self.db, email)

    async def get_all(self) -> UsersListResponse:
        return await crud_get_users(self.db)

    async def create(self, payload: UserCreate) -> User:
        new_user = await crud_create_user(self.db, payload)
        user_info_service = UserInfoService(self.db)

        await user_info_service.create(UserInfoCreate(user_id=new_user.id))

        return new_user

    async def require_admin(self, user: User) -> None:
        if user.role != user.role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required",
            )
