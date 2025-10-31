from fastapi import APIRouter, Depends
from app.schemas.admin import (
    CategoryOut,
    CategoryCreate,
    CategoriesListResponse,
    CategoryUpdate,
)
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies.service_factories import get_category_service_admin
from app.services.admin import CategoryService

router = APIRouter(tags=["categories"])


@router.get("/categories/{category_id}", response_model=CategoryOut)
async def read_category(
    category_id: int,
    svc_category: CategoryService = Depends(get_category_service_admin),
):
    return await svc_category.get(category_id)


@router.post(
    "/categories",
    response_model=CategoryOut,
)
async def add_category(
    new_category: CategoryCreate,
    svc_category: CategoryService = Depends(get_category_service_admin),
):
    return await svc_category.create(new_category)


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
)
async def read_categories(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc_category: CategoryService = Depends(get_category_service_admin),
):
    return await svc_category.get_all(offset, limit, q)


@router.patch("/categories/{category_id}", response_model=CategoryOut)
async def update_category_endpoint(
    category_id: int,
    payload: CategoryUpdate,
    svc_category: CategoryService = Depends(get_category_service_admin),
):
    return await svc_category.update(category_id, payload)


@router.delete("/categories/{category_id}")
async def delete_category_endpoint(
    category_id: int,
    svc_category: CategoryService = Depends(get_category_service_admin),
):
    await svc_category.delete(category_id)
