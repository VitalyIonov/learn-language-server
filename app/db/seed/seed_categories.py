import os
import mimetypes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.common import Category
from app.schemas.admin import UploadImageRequest
from app.services.admin import StorageR2Service, ImageService


def get_image_metadata(file_path: str) -> dict:
    size_bytes = os.path.getsize(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/jpeg"

    return {
        "size_bytes": size_bytes,
        "mime_type": mime_type,
    }


async def seed_categories(
    session: AsyncSession,
    data: list[dict],
    storage_service: StorageR2Service,
    image_service: ImageService,
):
    for category_data in data:
        result = await session.execute(
            select(Category).where(Category.name == category_data["name"])
        )

        if not result.scalar():
            image_asset = None
            image_path = category_data.get("image_path")

            if image_path and os.path.exists(image_path):
                try:
                    metadata = get_image_metadata(image_path)
                    image_asset = await image_service.create(
                        UploadImageRequest(
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

                        print(f"✅ Загружена картинка для {category_data['name']}")
                    else:
                        print(
                            f"❌ Не удалось загрузить картинку для {category_data['name']}"
                        )

                except Exception as e:
                    print(
                        f"❌ Ошибка при загрузке картинки для {category_data['name']}: {e}"
                    )

            category = Category(
                name=category_data["name"],
                image_id=image_asset.image_id if image_asset else None,
            )

            session.add(category)
            print(f"✅ Создана категория: {category.name}")

            # stmt = insert(Category).values(**category)
            # await session.execute(stmt)
    await session.commit()
