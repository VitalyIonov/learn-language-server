from fastapi import APIRouter, Depends
from app.core.dependencies.service_factories import get_current_user
from app.schemas.common import UserOut

router = APIRouter(tags=["users"])


@router.get("/current_user", response_model=UserOut)
async def read_user(
    current_user: UserOut = Depends(get_current_user),
):
    return current_user
