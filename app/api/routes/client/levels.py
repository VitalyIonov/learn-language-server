from fastapi import APIRouter, Depends, Query

from app.models import User
from app.schemas.admin import CategoryProgressInfoOut
from app.schemas.client import LevelsListResponse
from app.core.dependencies.common import get_current_user
from app.core.dependencies.client import get_level_service
from app.core.dependencies.admin import get_category_progress_info_service
from app.services.client import LevelService
from app.services.admin import CategoryProgressInfoService

router = APIRouter(tags=["levels"])


@router.get("/levels", response_model=LevelsListResponse)
async def read_levels(
    category_id: int = Query(None, description="Category ID"),
    svc: LevelService = Depends(get_level_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.get_all(user_id=current_user.id, category_id=category_id)


@router.post("/levels/unlock", response_model=CategoryProgressInfoOut)
async def unlock_level(
    category_id: int,
    level_id: int,
    svc_cpi: CategoryProgressInfoService = Depends(get_category_progress_info_service),
    current_user: User = Depends(get_current_user),
):
    return await svc_cpi.get_or_create(
        user_id=current_user.id, category_id=category_id, level_id=level_id
    )
