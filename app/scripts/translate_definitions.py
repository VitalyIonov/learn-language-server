import asyncio
from sqlalchemy import select, exists, func

from app.core.db import async_session
from app.models import Definition, Translation, Meaning, Category
from app.schemas.common import TranslationCreate
from app.services.common import TranslateService
from app.crud.common import (
    create_translation as crud_create_translation,
)

LANG_FROM = "es"
LANG_TO = "ru"


async def main():
    svc_translate = TranslateService()

    async with async_session() as session:
        stmt = (
            select(
                Definition.text,
                Category.name.label("category"),
                func.array_agg(func.distinct(Meaning.name)).label("meanings"),
            )
            .join(Definition.meanings)
            .join(Definition.category)
            .where(
                ~exists(
                    select(1).where(
                        (Translation.text == Definition.text)
                        & (Translation.lang_from == LANG_FROM)
                        & (Translation.lang_to == LANG_TO)
                    )
                )
            )
            .group_by(Definition.text, Category.name)
        )
        items = (await session.execute(stmt)).all()

        if not items:
            print("Нечего делать: все переводы уже созданы.")
            return

        print(f"Найдено {len(items)} записей без перевода.")

        ok = 0
        skipped = 0
        for item in items:
            meanings = ", ".join(item.meanings or [])
            context = f"{meanings} - {item.category or ''}".strip(" -")

            try:
                translated_text = await svc_translate.translate_by_open_ai(
                    text=item.text,
                    lang_from=LANG_FROM,
                    lang_to=LANG_TO,
                    context=context,
                )

                await crud_create_translation(
                    session,
                    TranslationCreate(
                        text=item.text,
                        translated_text=translated_text,
                        lang_from=LANG_FROM,
                        lang_to=LANG_TO,
                    ),
                )

                ok += 1
            except Exception as e:
                skipped += 1
                print(
                    f"[ERR] def_id={getattr(item, 'id', '?')}, ctx='{getattr(item, 'context', '?')}': {e!r}"
                )

        print(f"ok={ok}, failed={skipped}")


if __name__ == "__main__":
    asyncio.run(main())
