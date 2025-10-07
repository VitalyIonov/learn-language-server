from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.common import Category, Level, Meaning
from app.core.dependencies.admin import (
    get_tts_service,
    get_storage_r2_service,
    get_audio_service,
    get_meaning_service,
)
from app.utils.generate_audio import run_audio_generator


async def seed_meanings(session: AsyncSession, meanings_data: list[dict]) -> None:
    for m in meanings_data:
        exists = await session.execute(select(Meaning).where(Meaning.name == m["name"]))
        if exists.scalars().first():
            continue

        category_id = await session.scalar(
            select(Category.id).where(Category.name == m["category"])
        )
        level_id = await session.scalar(
            select(Level.id).where(Level.alias == m["level"])
        )

        session.add(
            Meaning(
                name=m["name"],
                category_id=category_id,
                level_id=level_id,
            )
        )

    rows = await session.execute(select(Meaning.id).where(Meaning.audio_id.is_(None)))
    ids_to_insert_audio: list[int] = [r[0] for r in rows]

    if not ids_to_insert_audio:
        return

    svc_storage_r2 = await get_storage_r2_service()
    svc_tts = await get_tts_service()
    svc_audio = await get_audio_service(
        db=session, svc_storage_r2=svc_storage_r2, svc_tts=svc_tts
    )
    svc_meaning = await get_meaning_service(db=session, svc_audio=svc_audio)

    await run_audio_generator(ids_to_insert_audio, svc_meaning.generate_audio)
