from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AudioAsset
from app.schemas.common import AudioAssetCreate, AudioAssetUpdate


async def get_audio(db: AsyncSession, audio_id: int) -> Optional[AudioAsset]:
    return await db.get(AudioAsset, audio_id)


async def get_audio_by_file_key(
    db: AsyncSession, file_key: str
) -> Optional[AudioAsset]:
    stmt = select(AudioAsset).where(AudioAsset.file_key == file_key)
    res = await db.execute(stmt)

    return res.scalars().first()


async def create_audio(db: AsyncSession, new_audio: AudioAssetCreate) -> AudioAsset:
    db_audio = AudioAsset(**new_audio.model_dump())
    db.add(db_audio)
    await db.commit()
    await db.refresh(db_audio)
    return db_audio


async def update_audio(
    db: AsyncSession, db_audio: AudioAsset, payload: AudioAssetUpdate
) -> AudioAsset:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_audio, field, value)
        await db.commit()
        await db.refresh(db_audio)
    return db_audio
