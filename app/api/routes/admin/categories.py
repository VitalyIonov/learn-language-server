from fastapi import APIRouter, Depends
from app.schemas.admin import CategoryOut, CategoryCreate, CategoriesListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies.admin import get_category_service
from app.services.admin import CategoryService


router = APIRouter(tags=["categories"])


@router.post(
    "/categories",
    response_model=CategoryOut,
)
async def add_category(
    new_category: CategoryCreate,
    svc: CategoryService = Depends(get_category_service),
):
    return await svc.create(new_category)


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
)
async def read_categories(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: CategoryService = Depends(get_category_service),
):
    return await svc.get_all(offset, limit, q)
