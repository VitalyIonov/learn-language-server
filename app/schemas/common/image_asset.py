from pydantic import ConfigDict

from app.models import AssetStatus
from app.schemas.common import BaseSchema


class ImageAssetOut(BaseSchema):
    id: int
    status: AssetStatus
    mime_type: str
    size_bytes: int
    alt: str
    width: int | None = None
    height: int | None = None
    file_key: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class ImageAssetUpload(BaseSchema):
    content_type: str
    size_bytes: int
    alt: str


class ImageAssetUploadOut(BaseSchema):
    upload_url: str
    file_key: str
    image_id: int


class ImageAssetCreate(BaseSchema):
    mime_type: str
    size_bytes: int
    file_key: str
    alt: str


class ImageAssetUpdate(BaseSchema):
    status: AssetStatus


class ImageAssetCommit(BaseSchema):
    image_id: int


class ImageAssetCommitOut(BaseSchema):
    image_url: str
