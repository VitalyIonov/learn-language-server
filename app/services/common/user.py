from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.crud.common import (
    get_user_by_email as crud_get_user_by_email,
    get_users as crud_get_users,
    create_user as crud_create_user,
)
from app.models.common import User
from app.schemas.common import UsersListResponse, UserCreate
from ..admin.user_info import UserInfoService
from ..admin.category_progress_info import CategoryProgressInfoService


class UserService:
    def __init__(
        self,
        db: AsyncSession,
        svc_cpi: CategoryProgressInfoService,
        svc_user_info: UserInfoService,
    ):
        self.db = db
        self.svc_cpi = svc_cpi
        self.svc_user_info = svc_user_info

    async def get_by_email(self, email: str) -> User | None:
        return await crud_get_user_by_email(self.db, email)

    async def get_all(self, offset: int, limit: int, q: str) -> UsersListResponse:
        return await crud_get_users(self.db, offset, limit, q)

    async def create(self, payload: UserCreate) -> User:
        new_user = await crud_create_user(self.db, payload)

        await self.svc_cpi.bootstrap(user_id=new_user.id)

        await self.db.commit()

        return new_user

    async def require_admin(self, user: User) -> None:
        if user.role != user.role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required",
            )
