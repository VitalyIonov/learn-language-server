from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_category_progress_info_service
from app.core.dependencies.common import get_current_user
from app.models import User
from app.schemas.client import CategoriesListResponse, CategoryOut
from app.core.dependencies.client import get_category_service
from app.services.admin import CategoryProgressInfoService
from app.services.client import CategoryService


router = APIRouter(tags=["categories"])


@router.get(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
async def read_category(
    category_id: int,
    svc_category: CategoryService = Depends(get_category_service),
    current_user: User = Depends(get_current_user),
):
    return await svc_category.get(current_user, category_id)


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
)
async def read_categories(
    svc: CategoryService = Depends(get_category_service),
):
    return await svc.get_all()
