from fastapi import APIRouter, Depends
from app.crud.category import get_categories, create_category
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas import CategoryOut, CategoryCreate, CategoriesListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


router = APIRouter(tags=["categories"])


@router.post(
    "/categories",
    response_model=CategoryOut,
)
async def add_category(
    new_category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_category(db, new_category)


@router.get(
    "/categories",
    response_model=CategoriesListResponse,
)
async def read_categories(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    return await get_categories(db, offset, limit, q)
