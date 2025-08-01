from fastapi import APIRouter, Depends
from app.schemas.admin import (
    DefinitionUpdate,
    DefinitionOutIds,
    DefinitionCreate,
    DefinitionListResponse,
)
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.services.admin import DefinitionService
from app.core.dependencies.admin import get_definition_service


router = APIRouter(tags=["definitions"])


@router.get("/definitions", response_model=DefinitionListResponse)
async def read_definitions(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: DefinitionService = Depends(get_definition_service),
):
    return await svc.get_all(offset, limit, q)


@router.get("/definitions/{definition_id}", response_model=DefinitionOutIds)
async def read_definition(
    definition_id: int,
    svc: DefinitionService = Depends(get_definition_service),
):
    return await svc.get(definition_id)


@router.post(
    "/definitions",
    response_model=DefinitionOutIds,
)
async def add_definition(
    payload: DefinitionCreate,
    svc: DefinitionService = Depends(get_definition_service),
):
    return await svc.create(payload)


@router.patch("/definitions/{definition_id}", response_model=DefinitionOutIds)
async def patch_definition(
    definition_id: int,
    payload: DefinitionUpdate,
    svc: DefinitionService = Depends(get_definition_service),
):
    return await svc.update(definition_id, payload)


@router.delete("/definitions/{definition_id}")
async def delete_definition_endpoint(
    definition_id: int,
    svc: DefinitionService = Depends(get_definition_service),
):
    return await svc.delete(definition_id)
