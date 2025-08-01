from fastapi import APIRouter, Depends
from typing import List
from app.core.dependencies.common import get_user_service, get_current_user
from app.schemas.common import UserOut
from app.services.common import UserService

router = APIRouter(tags=["users"])


@router.get("/users", response_model=List[UserOut])
async def read_users(
    svc: UserService = Depends(get_user_service),
):
    return await svc.get_all()


@router.get("/current_user", response_model=UserOut)
async def read_user(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user
