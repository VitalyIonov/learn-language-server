from __future__ import annotations

from typing import Iterable, List, Any, Callable, Awaitable
from fastapi import HTTPException


async def run_audio_generator(ids: Iterable[int], generate_audio: Callable[[int], Awaitable[Any]]) -> Any:
    ids_list: List[int] = list(ids)
    ok = 0
    skipped = 0

    for entity_id in ids_list:
        try:
            await generate_audio(entity_id)
            ok += 1
            print(f"[OK] id={entity_id}")
        except HTTPException as e:
            if e.status_code == 400:
                skipped += 1
                print(f"[SKIP] id={entity_id} — уже сгенерировано")
            else:
                print(f"[ERR] id={entity_id}: {e.status_code} {e.detail}")
                raise

    print(
        f"Готово. Аудио: успешно={ok}, пропущено={skipped}, всего={len(ids_list)}"
    )
