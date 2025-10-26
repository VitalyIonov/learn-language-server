import os
import mimetypes

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.common import Category
from app.schemas.common import ImageAssetUploadPayload
from app.services.admin import ImageService


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
    image_service: ImageService,
):
    for category_data in data:
        existing_category = await session.scalar(
            select(Category).where(Category.name == category_data["name"])
        )

        if existing_category and existing_category.image_id:
            continue

        image_asset = None
        image_path = category_data.get("image_path")

        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as file_obj:
                    upload_file = UploadFile(
                        filename=os.path.basename(image_path),
                        file=file_obj,
                    )
                    image_asset = await image_service.create_and_upload(
                        file=upload_file,
                        payload=ImageAssetUploadPayload(text=category_data.get("name")),
                    )

            except Exception as e:
                print(
                    f"❌ Ошибка при загрузке картинки {category_data['image_path']}: {e}"
                )

        if existing_category and not existing_category.image_id and image_asset:
            existing_category.image_id = image_asset.image_id

            session.add(existing_category)
            continue

        result = Category(
            name=category_data["name"],
            image_id=image_asset.image_id if image_asset else None,
        )

        session.add(result)
    await session.commit()
