from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.admin import DefinitionUpdate, DefinitionListResponse, DefinitionCreate
from app.crud.admin import (
    get_definition as get_definition_crud,
    get_definitions as get_definitions_crud,
    create_definition as create_definition_crud,
    update_definition as update_definition_crud,
    delete_definition as delete_definition_crud,
)

from app.models.common import Definition


class DefinitionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, definition_id: int) -> Definition:
        result = await get_definition_crud(self.db, definition_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Definition not found")
        return result

    async def get_all(self, offset: int, limit: int, q: str) -> DefinitionListResponse:
        return await get_definitions_crud(self.db, offset, limit, q)

    async def update(self, definition_id: int, payload: DefinitionUpdate):
        result = await get_definition_crud(self.db, definition_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Definition not found")
        return await update_definition_crud(self.db, result, payload)

    async def create(self, payload: DefinitionCreate) -> Definition:
        return await create_definition_crud(self.db, payload)

    async def delete(self, definition_id: int):
        success = await delete_definition_crud(self.db, definition_id)
        if not success:
            raise HTTPException(status_code=404, detail="Definition not found")
