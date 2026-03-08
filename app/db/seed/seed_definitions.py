import os
from typing import Union

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import (
    Category,
    Level,
    Meaning,
    TextDefinition,
    ImageDefinition,
    QuestionTypeName,
)
from app.schemas.common import ImageAssetUploadPayload
from app.services.admin import ImageService
from app.core.dependencies.service_factories import (
    get_tts_service,
    get_storage_r2_service,
    get_audio_service,
    get_text_definition_service,
)
from app.core.db import async_session as session_factory
from app.utils.generate_audio import run_audio_generator


async def seed_definitions(
    session: AsyncSession,
    data: list[dict],
    image_service: ImageService,
) -> None:
    for definition_data in data:
        category_id = await session.scalar(
            select(Category.id).where(Category.name == definition_data["category"])
        )
        level_id = await session.scalar(
            select(Level.id).where(Level.alias == definition_data["level"])
        )
        meaning_objs = (
            await session.scalars(
                select(Meaning).where(Meaning.name.in_(definition_data["meanings"]))
            )
        ).all()

        def_type = definition_data.get("type", "").upper()

        result: Union[TextDefinition, ImageDefinition] | None = None

        if def_type == QuestionTypeName.TEXT.upper():
            existing_text_def: TextDefinition | None = await session.scalar(
                select(TextDefinition).where(TextDefinition.text == definition_data["text"])
            )

            if existing_text_def:
                existing_text_def.meanings.extend(meaning_objs)

                continue

            result = TextDefinition(
                text=definition_data["text"],
                category_id=category_id,
                level_id=level_id,
                language=definition_data["language"],
                group=definition_data["group"],
            )

        if def_type == QuestionTypeName.IMAGE.upper():
            existing_img_def: ImageDefinition | None = await session.scalar(
                select(ImageDefinition).where(ImageDefinition.text == definition_data["text"])
            )

            if existing_img_def and existing_img_def.image_id:
                existing_img_def.meanings.extend(meaning_objs)

                continue

            image_asset = None
            image_path = definition_data.get("image_path")

            if image_path and os.path.exists(image_path):
                try:
                    with open(image_path, "rb") as file_obj:
                        upload_file = UploadFile(
                            filename=os.path.basename(image_path),
                            file=file_obj,
                        )
                        image_asset = await image_service.create_and_upload(
                            file=upload_file,
                            payload=ImageAssetUploadPayload(text=definition_data.get("text")),
                        )

                except Exception as e:
                    print(f"❌ Ошибка при загрузке картинки {definition_data['image_path']}: {e}")

            if existing_img_def and not existing_img_def.image_id and image_asset:
                existing_img_def.image_id = image_asset.image_id

                existing_img_def.meanings.extend(meaning_objs)

                session.add(existing_img_def)
                continue

            result = ImageDefinition(
                image_id=image_asset.image_id if image_asset else None,
                text=definition_data["text"],
                category_id=category_id,
                level_id=level_id,
                language=definition_data["language"],
                group=definition_data["group"],
            )

        if result:
            result.meanings.extend(meaning_objs)
            session.add(result)

    await session.commit()

    rows = await session.execute(
        select(TextDefinition.id).where(TextDefinition.audio_id.is_(None))
    )
    ids_to_insert_audio: list[int] = [r[0] for r in rows]

    if not ids_to_insert_audio:
        return

    async def generate_audio_for_definition(definition_id: int) -> None:
        async with session_factory() as db:
            svc_storage_r2 = await get_storage_r2_service()
            svc_tts = await get_tts_service()
            svc_audio = await get_audio_service(db=db, svc_storage_r2=svc_storage_r2, svc_tts=svc_tts)
            svc_text_definitions = await get_text_definition_service(db=db, svc_audio=svc_audio)
            await svc_text_definitions.generate_audio(definition_id=definition_id)

    await run_audio_generator(ids_to_insert_audio, generate_audio_for_definition)
