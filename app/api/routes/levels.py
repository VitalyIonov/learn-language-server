from fastapi import APIRouter, Depends
from app.crud.level import get_levels, create_level
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas import LevelOut, LevelCreate, LevelsListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


router = APIRouter(tags=["levels"])


@router.post("/levels", response_model=LevelOut)
async def add_level(
    new_level: LevelCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_level(db, new_level)


@router.get("/levels", response_model=LevelsListResponse)
async def read_levels(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    return await get_levels(db, offset, limit, q)
