import asyncio

from fastapi import HTTPException, UploadFile
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.crud.admin import (
    get_image as crud_get_image,
    create_image as crud_create_image,
    update_image as crud_update_image,
    get_image_by_file_key as crud_get_image_by_file_key,
)
from app.models import ImageAsset, AssetStatus
from app.schemas.common import (
    ImageAssetUploadOut,
    ImageAssetUploadInit,
    ImageAssetUploadInitOut,
    ImageAssetCreate,
    ImageAssetUpdate,
    ImageAssetUploadPayload,
)
from app.constants.data import MAX_IMAGE_SIZE_BYTES
from app.services.admin import StorageR2Service
from app.utils import make_image_file_hash


class ImageService:
    def __init__(self, db: AsyncSession, svc_storage_r2: StorageR2Service):
        self.db = db
        self.svc_storage_r2 = svc_storage_r2

    async def get(self, image_id: int) -> ImageAsset:
        entity = await crud_get_image(self.db, image_id)

        if entity is None:
            raise HTTPException(404, "Image not found")

        return entity

    async def create(self, payload: ImageAssetUploadInit) -> ImageAssetUploadInitOut:
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
                alt=payload.alt,
                file_key=file_key,
            ),
        )

        return ImageAssetUploadInitOut(
            upload_url=url, file_key=file_key, image_id=image.id
        )

    async def create_and_upload(
        self, file: UploadFile, payload: ImageAssetUploadPayload
    ) -> ImageAssetUploadOut:
        if file.content_type and not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Unsupported file type",
            )

        await file.seek(0)

        content_type = file.content_type or "application/octet-stream"
        file_key = await asyncio.to_thread(make_image_file_hash, file.file)

        image = await self._get_by_file_key(file_key)

        if image and image.status == AssetStatus.READY:
            return ImageAssetUploadOut(image_url=str(image.url), image_id=image.id)

        await file.seek(0)

        is_upload_success = await self.svc_storage_r2.upload_file(
            file_key, file.file, content_type
        )

        if not is_upload_success:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Storage upload failed",
            )

        if image:
            await self.commit(image.id)

            return ImageAssetUploadOut(image_url=str(image.url), image_id=image.id)

        image = await self._create_image_from_existing_file(
            file_key, content_type, payload.text
        )

        return ImageAssetUploadOut(image_url=str(image.url), image_id=image.id)

    async def commit(self, image_id: int) -> ImageAsset:
        image = await self.get(image_id)

        if image.status == AssetStatus.READY:
            return image

        return await crud_update_image(
            self.db, image, ImageAssetUpdate(status=AssetStatus.READY)
        )

    async def _get_by_file_key(self, file_key: str) -> ImageAsset | None:
        return await crud_get_image_by_file_key(self.db, file_key)

    async def _create_image_from_existing_file(
        self, file_key: str, content_type: str, text: str
    ) -> ImageAsset:
        file_metadata = await self.svc_storage_r2.get_file_metadata(file_key)
        updated_content_type = (
            file_metadata.get("content_type") if file_metadata else content_type
        )

        return await crud_create_image(
            self.db,
            ImageAssetCreate(
                mime_type=updated_content_type,
                alt=text,
                file_key=file_key,
                status=AssetStatus.READY,
            ),
        )
