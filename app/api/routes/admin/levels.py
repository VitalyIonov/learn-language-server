from fastapi import APIRouter, Depends
from app.schemas.admin import LevelOut, LevelCreate, LevelsListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies.admin import get_level_service
from app.services.admin import LevelService

router = APIRouter(tags=["levels"])


@router.post("/levels", response_model=LevelOut)
async def add_level(
    new_level: LevelCreate,
    svc: LevelService = Depends(get_level_service),
):
    return await svc.create(new_level)


@router.get("/levels", response_model=LevelsListResponse)
async def read_levels(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: LevelService = Depends(get_level_service),
):
    return await svc.get_all(offset, limit, q)


@router.delete("/levels/{level_id}")
async def delete_level_endpoint(
    level_id: int,
    svc: LevelService = Depends(get_level_service),
):
    await svc.delete(level_id)
