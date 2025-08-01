from fastapi import APIRouter, Depends
from app.schemas.admin import CategoriesListResponse
from app.core.dependencies.client import get_category_service
from app.services.client import CategoryService


router = APIRouter(tags=["categories"])


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
)
async def read_categories(
    svc: CategoryService = Depends(get_category_service),
):
    return await svc.get_all()
