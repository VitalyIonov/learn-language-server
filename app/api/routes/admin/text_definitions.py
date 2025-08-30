from fastapi import APIRouter, Depends
from app.schemas.admin import (
    TextDefinitionUpdate,
    TextDefinitionOutIds,
    TextDefinitionCreate,
    TextDefinitionListResponse,
)
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.services.admin import TextDefinitionService
from app.core.dependencies.admin import get_text_definition_service


router = APIRouter(tags=["text_definitions"])


@router.get("/text_definitions", response_model=TextDefinitionListResponse)
async def read_text_definitions(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: TextDefinitionService = Depends(get_text_definition_service),
):
    return await svc.get_all(offset, limit, q)


@router.get("/text_definitions/{definition_id}", response_model=TextDefinitionOutIds)
async def read_text_definition(
    definition_id: int,
    svc: TextDefinitionService = Depends(get_text_definition_service),
):
    return await svc.get(definition_id)


@router.post(
    "/text_definitions",
    response_model=TextDefinitionOutIds,
)
async def add_text_definition(
    payload: TextDefinitionCreate,
    svc: TextDefinitionService = Depends(get_text_definition_service),
):
    return await svc.create(payload)


@router.patch("/text_definitions/{definition_id}", response_model=TextDefinitionOutIds)
async def patch_text_definition(
    definition_id: int,
    payload: TextDefinitionUpdate,
    svc: TextDefinitionService = Depends(get_text_definition_service),
):
    return await svc.update(definition_id, payload)


@router.delete("/text_definitions/{definition_id}")
async def delete_text_definition(
    definition_id: int,
    svc: TextDefinitionService = Depends(get_text_definition_service),
):
    return await svc.delete(definition_id)
