from fastapi import APIRouter, Depends
from app.schemas.admin import (
    ImageDefinitionUpdate,
    ImageDefinitionOut,
    ImageDefinitionCreate,
    ImageDefinitionListResponse,
)
from fastapi import Query
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.services.admin import ImageDefinitionService
from app.core.dependencies.admin import get_image_definition_service


router = APIRouter(tags=["text_definitions"])


@router.get("/image_definitions", response_model=ImageDefinitionListResponse)
async def read_image_definitions(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: ImageDefinitionService = Depends(get_image_definition_service),
):
    return await svc.get_all(offset, limit, q)


@router.get("/image_definitions/{definition_id}", response_model=ImageDefinitionOut)
async def read_image_definition(
    definition_id: int,
    svc: ImageDefinitionService = Depends(get_image_definition_service),
):
    return await svc.get(definition_id)


@router.post(
    "/image_definitions",
    response_model=ImageDefinitionOut,
)
async def add_image_definition(
    payload: ImageDefinitionCreate,
    svc: ImageDefinitionService = Depends(get_image_definition_service),
):
    return await svc.create(payload)


@router.patch("/image_definitions/{definition_id}", response_model=ImageDefinitionOut)
async def patch_image_definition(
    definition_id: int,
    payload: ImageDefinitionUpdate,
    svc: ImageDefinitionService = Depends(get_image_definition_service),
):
    return await svc.update(definition_id, payload)


@router.delete("/image_definitions/{definition_id}")
async def delete_image_definition(
    definition_id: int,
    svc: ImageDefinitionService = Depends(get_image_definition_service),
):
    return await svc.delete(definition_id)
