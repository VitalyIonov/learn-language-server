from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import DefinitionUpdate
from app.crud.definition import (
    get_definition as get_definition_crud,
    update_definition as update_definition_crud,
    delete_definition as delete_definition_crud,
)


async def get_definition(db: AsyncSession, definition_id: int):
    result = await get_definition_crud(db, definition_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Definition not found")
    return result


async def update_definition(
    db: AsyncSession, definition_id: int, payload: DefinitionUpdate
):
    result = await get_definition_crud(db, definition_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Definition not found")
    return await update_definition_crud(db, result, payload)


async def delete_definition(db: AsyncSession, definition_id: int):
    success = await delete_definition_crud(db, definition_id)
    if not success:
        raise HTTPException(status_code=404, detail="Definition not found")
