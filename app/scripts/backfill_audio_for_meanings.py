import asyncio
from sqlalchemy import select
from fastapi import HTTPException

from app.core.db import async_session
from app.models import Meaning
from app.core.dependencies.service_factories import (
    get_tts_service,
    get_storage_r2_service,
    get_audio_service,
    get_meaning_service,
)


async def main():
    async with async_session() as session:
        svc_storage_r2 = await get_storage_r2_service()
        svc_tts = await get_tts_service()
        svc_audio = await get_audio_service(
            db=session, svc_storage_r2=svc_storage_r2, svc_tts=svc_tts
        )
        svc_meaning = await get_meaning_service(db=session, svc_audio=svc_audio)

        result = await session.execute(
            select(Meaning.id).where(Meaning.audio_id.is_(None))
        )
        ids = [row[0] for row in result]
        if not ids:
            print("Нечего делать: все записи уже с аудио.")
            return

        print(f"Найдено {len(ids)} записей без аудио.")
        ok = 0
        skipped = 0

        for mid in ids:
            try:
                await svc_meaning.generate_audio(mid)
                ok += 1
                print(f"[OK] meaning_id={mid}")
            except HTTPException as e:
                if e.status_code == 400:
                    skipped += 1
                    print(f"[SKIP] meaning_id={mid} — уже сгенерировано")
                else:
                    print(f"[ERR] meaning_id={mid}: {e.status_code} {e.detail}")
                    raise

        print(f"Готово. Успешно: {ok}, пропущено: {skipped}, всего: {len(ids)}")


if __name__ == "__main__":
    asyncio.run(main())
