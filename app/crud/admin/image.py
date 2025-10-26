from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ImageAsset
from app.schemas.common import ImageAssetCreate, ImageAssetUpdate


async def get_image(db: AsyncSession, image_id: int) -> Optional[ImageAsset]:
    return await db.get(ImageAsset, image_id)


async def get_image_by_file_key(
    db: AsyncSession, file_key: str
) -> Optional[ImageAsset]:
    stmt = select(ImageAsset).where(ImageAsset.file_key == file_key)
    res = await db.execute(stmt)

    return res.scalars().first()


async def create_image(db: AsyncSession, new_image: ImageAssetCreate) -> ImageAsset:
    db_image = ImageAsset(**new_image.model_dump())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image


async def update_image(
    db: AsyncSession, db_image: ImageAsset, payload: ImageAssetUpdate
) -> ImageAsset:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_image, field, value)
        await db.commit()
        await db.refresh(db_image)
    return db_image
