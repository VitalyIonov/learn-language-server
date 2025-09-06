from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_image_service
from app.schemas.common import (
    ImageAssetUpload,
    ImageAssetUploadOut,
    ImageAssetCommit,
    ImageAssetCommitOut,
)
from app.services.admin import ImageService
from app.utils.url_generator import public_url

router = APIRouter(tags=["images"])


@router.post("/images/upload-init", response_model=ImageAssetUploadOut)
async def init_image_upload(
    body: ImageAssetUpload,
    svc_image: ImageService = Depends(get_image_service),
):
    return await svc_image.create(payload=body)


@router.post("/images/upload-commit", response_model=ImageAssetCommitOut)
async def commit_image_upload(
    payload: ImageAssetCommit,
    svc_image: ImageService = Depends(get_image_service),
):
    image = await svc_image.commit(payload.image_id)

    image_url = public_url(image.file_key)

    return ImageAssetCommitOut(image_url=image_url)
