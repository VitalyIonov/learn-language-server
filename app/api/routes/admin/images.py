from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_image_service, get_storage_r2_service
from app.schemas.admin import (
    UploadImageResponse,
    UploadImageRequest,
    CommitImageResponse,
    CommitImageRequest,
)
from app.services.admin import ImageService, StorageR2Service
from app.utils.url_generator import public_url

router = APIRouter(tags=["images"])


@router.post("/images/upload-init", response_model=UploadImageResponse)
async def init_image_upload(
    body: UploadImageRequest,
    svc_image: ImageService = Depends(get_image_service),
):
    return await svc_image.create(payload=body)


@router.post("/images/upload-commit", response_model=CommitImageResponse)
async def commit_image_upload(
    payload: CommitImageRequest,
    svc_image: ImageService = Depends(get_image_service),
):
    image = await svc_image.commit(payload.image_id)

    image_url = public_url(image.file_key)

    return CommitImageResponse(image_url=image_url)
