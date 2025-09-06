import os
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.seed import get_image_metadata
from app.models import (
    Category,
    Level,
    Meaning,
    TextDefinition,
    ImageDefinition,
    QuestionTypeName,
)
from app.schemas.common import ImageAssetUpload
from app.services.admin import StorageR2Service, ImageService


async def seed_definitions(
    session: AsyncSession,
    data: list[dict],
    storage_service: StorageR2Service,
    image_service: ImageService,
) -> None:
    for item in data:
        category_id = await session.scalar(
            select(Category.id).where(Category.name == item["category"])
        )
        level_id = await session.scalar(
            select(Level.id).where(Level.alias == item["level"])
        )
        meaning_objs = (
            await session.scalars(
                select(Meaning).where(Meaning.name.in_(item["meanings"]))
            )
        ).all()

        def_type = item.get("type")

        result: Union[TextDefinition, ImageDefinition] | None = None

        if def_type == QuestionTypeName.TEXT:
            result = TextDefinition(
                text=item["text"],
                category_id=category_id,
                level_id=level_id,
            )

        if def_type == QuestionTypeName.IMAGE:
            image_asset = None
            image_path = item.get("image_path")

            if image_path and os.path.exists(image_path):
                try:
                    metadata = get_image_metadata(image_path)
                    image_asset = await image_service.create(
                        ImageAssetUpload(
                            content_type=metadata["mime_type"],
                            size_bytes=metadata["size_bytes"],
                        )
                    )

                    with open(image_path, "rb") as file_obj:
                        upload_success = await storage_service.upload_file(
                            image_asset.file_key, file_obj, metadata["mime_type"]
                        )

                    if upload_success:
                        await image_service.commit(image_asset.image_id)
                    else:
                        print(f"❌ Не удалось загрузить картинку {item['image_path']}")

                except Exception as e:
                    print(f"❌ Ошибка при загрузке картинки {item['image_path']}: {e}")

            result = ImageDefinition(
                image_id=image_asset.image_id if image_asset else None,
                category_id=category_id,
                level_id=level_id,
            )

        result.meanings.extend(meaning_objs) if result else None
        session.add(result)
    await session.commit()
