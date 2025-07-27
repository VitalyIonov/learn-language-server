from fastapi import APIRouter, Depends
from app.crud.user import get_users
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.core.db import get_db
from app.schemas import UserOut
from typing import List

router = APIRouter(tags=["users"])


@router.get("/users", response_model=List[UserOut])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@router.get("/current_user", response_model=UserOut)
async def read_user(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user
