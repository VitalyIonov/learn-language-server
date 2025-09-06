from fastapi import HTTPException
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.admin import (
    get_image as crud_get_image,
    create_image as crud_create_image,
    update_image as crud_update_image,
)
from app.models import ImageAsset, AssetStatus
from app.schemas.common import (
    ImageAssetUpload,
    ImageAssetUploadOut,
    ImageAssetCreate,
    ImageAssetUpdate,
)
from app.constants.data import MAX_IMAGE_SIZE_BYTES
from app.services.admin import StorageR2Service


class ImageService:
    def __init__(self, db: AsyncSession, svc_storage_r2: StorageR2Service):
        self.db = db
        self.svc_storage_r2 = svc_storage_r2

    async def get(self, image_id: int) -> ImageAsset:
        entity = await crud_get_image(self.db, image_id)

        if entity is None:
            raise HTTPException(404, "Image not found")

        return entity

    async def create(self, payload: ImageAssetUpload) -> ImageAssetUploadOut:
        if (
            not payload.content_type.startswith("image/")
            or payload.size_bytes > MAX_IMAGE_SIZE_BYTES
        ):
            raise HTTPException(400, "Invalid image")

        file_key = uuid4().hex
        url = self.svc_storage_r2.presign_put(file_key, payload.content_type)

        image = await crud_create_image(
            self.db,
            ImageAssetCreate(
                mime_type=payload.content_type,
                size_bytes=payload.size_bytes,
                file_key=file_key,
            ),
        )

        return ImageAssetUploadOut(upload_url=url, file_key=file_key, image_id=image.id)

    async def commit(self, image_id: int) -> ImageAsset:
        image = await self.get(image_id)

        if image.status == AssetStatus.READY:
            return image

        return await crud_update_image(
            self.db, image, ImageAssetUpdate(status=AssetStatus.READY)
        )
