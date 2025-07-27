from fastapi import APIRouter, Depends, status, Body
from app.schemas import MeaningOut, MeaningCreate, MeaningUpdate, MeaningsListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies import get_meaning_service
from app.services.meaning import MeaningService


router = APIRouter(tags=["meanings"])


@router.get("/meanings", response_model=MeaningsListResponse)
async def read_meanings(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: MeaningService = Depends(get_meaning_service),
):
    return await svc.get_all(offset, limit, q)


@router.get("/meanings/{meaning_id}", response_model=MeaningOut)
async def read_meaning(
    meaning_id: int,
    svc: MeaningService = Depends(get_meaning_service),
):
    return await svc.get(meaning_id)


@router.post(
    "/meanings",
    response_model=MeaningOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую сущность Meaning",
)
async def add_meaning(
    payload: MeaningCreate,
    svc: MeaningService = Depends(get_meaning_service),
):
    return await svc.create(payload)


@router.patch("/meanings/{meaning_id}", response_model=MeaningOut)
async def update_meaning_endpoint(
    meaning_id: int,
    payload: MeaningUpdate = Body(..., description="Данные для обновления Meaning"),
    svc: MeaningService = Depends(get_meaning_service),
):
    return await svc.update(meaning_id, payload)


@router.delete("/meanings/{meaning_id}")
async def delete_meaning_endpoint(
    meaning_id: int,
    svc: MeaningService = Depends(get_meaning_service),
):
    await svc.delete(meaning_id)
