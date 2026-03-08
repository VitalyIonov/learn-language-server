from __future__ import annotations

import asyncio
from typing import Iterable, List, Any, Callable, Awaitable
from fastapi import HTTPException


async def run_audio_generator(
    ids: Iterable[int],
    generate_audio: Callable[[int], Awaitable[Any]],
    max_concurrency: int = 5,
) -> None:
    ids_list: List[int] = list(ids)
    ok = 0
    skipped = 0
    failed = 0
    semaphore = asyncio.Semaphore(max_concurrency)

    async def process(entity_id: int) -> None:
        nonlocal ok, skipped, failed
        async with semaphore:
            try:
                await generate_audio(entity_id)
                ok += 1
                print(f"[OK] id={entity_id}")
            except HTTPException as e:
                if e.status_code == 400:
                    skipped += 1
                    print(f"[SKIP] id={entity_id} — уже сгенерировано")
                else:
                    failed += 1
                    print(f"[ERR] id={entity_id}: {e.status_code} {e.detail}")

    await asyncio.gather(*[process(entity_id) for entity_id in ids_list])

    print(
        f"Готово. Аудио: успешно={ok}, пропущено={skipped}, ошибок={failed}, всего={len(ids_list)}"
    )
