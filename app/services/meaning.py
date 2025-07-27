from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import MeaningUpdate
from app.crud.meaning import get_meaning, update_meaning as update_meaning_crud


async def update_meaning(db: AsyncSession, meaning_id: int, payload: MeaningUpdate):
    meaning = await get_meaning(db, meaning_id)
    if meaning is None:
        raise HTTPException(status_code=404, detail="Meaning not found")
    return await update_meaning_crud(db, meaning, payload)
