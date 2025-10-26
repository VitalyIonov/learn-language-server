from fastapi import APIRouter, Depends, UploadFile, File

from app.core.dependencies.admin import get_image_service
from app.schemas.common import (
    ImageAssetUploadInit,
    ImageAssetUploadInitOut,
    ImageAssetUploadOut,
    ImageAssetCommit,
    ImageAssetCommitOut,
)
from app.services.admin import ImageService
from app.utils.url_generator import public_url

router = APIRouter(tags=["images"])


@router.post("/images/upload-init", response_model=ImageAssetUploadInitOut)
async def init_image_upload(
    body: ImageAssetUploadInit,
    svc_image: ImageService = Depends(get_image_service),
):
    return await svc_image.create(payload=body)


@router.post("/images/upload", response_model=ImageAssetUploadOut)
async def image_upload(
    file: UploadFile = File(...),
    svc_image: ImageService = Depends(get_image_service),
):
    return await svc_image.create_and_upload(file=file)


@router.post("/images/upload-commit", response_model=ImageAssetCommitOut)
async def commit_image_upload(
    payload: ImageAssetCommit,
    svc_image: ImageService = Depends(get_image_service),
):
    image = await svc_image.commit(payload.image_id)

    image_url = public_url(image.file_key)

    return ImageAssetCommitOut(image_url=image_url)
