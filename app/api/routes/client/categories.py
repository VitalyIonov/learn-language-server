from fastapi import APIRouter, Depends

from app.models import User
from app.schemas.client import CategoriesListResponse, CategoryOut
from app.core.dependencies.service_factories import (
    get_category_service_client,
    get_current_user,
)
from app.services.client import CategoryService


router = APIRouter(tags=["categories"])


@router.get(
    "/categories/{category_id}", response_model=CategoryOut, operation_id="getCategory"
)
async def read_category(
    category_id: int,
    svc_category: CategoryService = Depends(get_category_service_client),
    current_user: User = Depends(get_current_user),
):
    return await svc_category.get(current_user, category_id)


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
    operation_id="getCategoriesList",
)
async def read_categories(
    svc: CategoryService = Depends(get_category_service_client),
):
    return await svc.get_all()
