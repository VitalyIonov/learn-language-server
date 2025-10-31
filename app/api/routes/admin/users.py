from fastapi import APIRouter, Depends, Query

from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies.service_factories import get_user_service, get_current_user
from app.schemas.common import UserOut, UsersListResponse
from app.services.common import UserService

router = APIRouter(tags=["users"])


@router.get("/users", response_model=UsersListResponse)
async def read_users(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: UserService = Depends(get_user_service),
):
    return await svc.get_all(offset, limit, q)


@router.get("/current_user", response_model=UserOut)
async def read_user(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user
