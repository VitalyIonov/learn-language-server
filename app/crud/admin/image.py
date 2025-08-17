from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Asset
from app.schemas.admin import ImageCreate, ImageUpdate


async def get_image(db: AsyncSession, image_id: int) -> Optional[Asset]:
    return await db.get(Asset, image_id)


async def create_image(db: AsyncSession, new_image: ImageCreate):
    db_image = Asset(**new_image.model_dump())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image


async def update_image(
    db: AsyncSession, db_image: Asset, payload: ImageUpdate
) -> Asset:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_image, field, value)
        await db.commit()
        await db.refresh(db_image)
    return db_image
