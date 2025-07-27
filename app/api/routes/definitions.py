from fastapi import APIRouter, Depends, Body
from app.crud.definition import (
    get_definitions,
    create_definition,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas import (
    DefinitionUpdate,
    DefinitionOutIds,
    DefinitionCreate,
    DefinitionListResponse,
)
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.services.definition import (
    update_definition as update_service,
    delete_definition as delete_service,
    get_definition as get_definition_service,
)


router = APIRouter(tags=["definitions"])


@router.get("/definitions", response_model=DefinitionListResponse)
async def read_definitions(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    return await get_definitions(db, offset, limit, q)


@router.get("/definitions/{definition_id}", response_model=DefinitionOutIds)
async def read_definition(
    definition_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await get_definition_service(db, definition_id)


@router.post(
    "/definitions",
    response_model=DefinitionOutIds,
)
async def add_definition(
    payload: DefinitionCreate = Body(
        ..., description="Данные для создания нового Definition"
    ),
    db: AsyncSession = Depends(get_db),
):
    return await create_definition(db, payload)


@router.patch("/definitions/{definition_id}", response_model=DefinitionOutIds)
async def patch_definition(
    definition_id: int,
    payload: DefinitionUpdate = Body(
        ..., description="Данные для обновления Definition"
    ),
    db: AsyncSession = Depends(get_db),
):
    return await update_service(db, definition_id, payload)


@router.delete("/definitions/{definition_id}")
async def delete_definition_endpoint(
    definition_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await delete_service(db, definition_id)
