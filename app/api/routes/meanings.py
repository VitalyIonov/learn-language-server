from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.crud.meaning import (
    create_meaning,
    get_meanings,
    delete_meaning,
    get_meaning,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas import MeaningOut, MeaningCreate, MeaningUpdate, MeaningsListResponse
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.services.meaning import update_meaning as update_service


router = APIRouter(tags=["meanings"])


@router.get("/meanings", response_model=MeaningsListResponse)
async def read_meanings(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    return await get_meanings(db, offset, limit, q)


@router.get("/meanings/{meaning_id}", response_model=MeaningOut)
async def read_meaning(
    meaning_id: int,
    db: AsyncSession = Depends(get_db),
):
    meaning = await get_meaning(db, meaning_id)
    if meaning is None:
        raise HTTPException(status_code=404, detail="Meaning not found")
    return meaning


@router.post(
    "/meanings",
    response_model=MeaningOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую сущность Meaning",
)
async def add_meaning(
    payload: MeaningCreate = Body(
        ..., description="Данные для создания нового Meaning"
    ),
    db: AsyncSession = Depends(get_db),
):
    return await create_meaning(db, payload)


@router.patch("/meanings/{meaning_id}", response_model=MeaningOut)
async def update_meaning_endpoint(
    meaning_id: int,
    payload: MeaningUpdate = Body(..., description="Данные для обновления Meaning"),
    db: AsyncSession = Depends(get_db),
):
    updated = await update_service(db, meaning_id, payload)
    return updated


@router.delete("/meanings/{meaning_id}")
async def delete_meaning_endpoint(
    meaning_id: int,
    db: AsyncSession = Depends(get_db),
):
    success = await delete_meaning(db, meaning_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meaning not found")
