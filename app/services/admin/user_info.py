from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models.common import UserInfo
from app.schemas.admin import UserInfoCreate, UserInfoUpdate
from app.crud.admin import (
    get_user_info as crud_get_user_info,
    create_user_info as crud_create_user_info,
    update_user_info as crud_update_user_info,
)


class UserInfoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, user_id: int) -> UserInfo:
        entity = await crud_get_user_info(self.db, user_id)
        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="UserInfo not found"
            )
        return entity

    async def create(self, payload: UserInfoCreate) -> None:
        entity = await crud_get_user_info(self.db, payload.user_id)

        if entity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="UserInfo already created",
            )

        await crud_create_user_info(self.db, payload)

    async def update(self, user_id: int, payload: UserInfoUpdate) -> UserInfo:
        entity = await self.get(user_id)

        return await crud_update_user_info(self.db, entity, payload)
