from fastapi import APIRouter, Depends, Query

from app.models import User
from app.schemas.client import LevelsListResponse
from app.core.dependencies.service_factories import (
    get_current_user,
    get_level_service_client,
)
from app.services.client import LevelService

router = APIRouter(tags=["levels"])


@router.get("/levels", response_model=LevelsListResponse, operation_id="getLevelsList")
async def read_levels(
    category_id: int = Query(None, description="Category ID"),
    svc: LevelService = Depends(get_level_service_client),
    current_user: User = Depends(get_current_user),
):
    return await svc.get_all(user_id=current_user.id, category_id=category_id)
