from typing import Optional

from pydantic import ConfigDict

from app.models import AssetStatus
from app.schemas.base import BaseSchema


class ImageAssetOut(BaseSchema):
    id: int
    status: AssetStatus
    mime_type: str
    size_bytes: int | None = None
    alt: str
    width: int | None = None
    height: int | None = None
    file_key: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class ImageAssetUploadInit(BaseSchema):
    content_type: str
    size_bytes: int
    alt: str


class ImageAssetUploadInitOut(BaseSchema):
    upload_url: str
    file_key: str
    image_id: int


class ImageAssetUploadPayload(BaseSchema):
    text: str


class ImageAssetUploadOut(BaseSchema):
    image_id: int
    image_url: str


class ImageAssetCreate(BaseSchema):
    mime_type: str
    file_key: str
    alt: str
    size_bytes: Optional[int] = None
    status: Optional[AssetStatus] = None


class ImageAssetUpdate(BaseSchema):
    status: AssetStatus


class ImageAssetCommit(BaseSchema):
    image_id: int


class ImageAssetCommitOut(BaseSchema):
    image_url: str
