from app.models import AssetStatus
from app.schemas.common import BaseSchema


class UploadImageRequest(BaseSchema):
    content_type: str
    size_bytes: int


class UploadImageResponse(BaseSchema):
    upload_url: str
    file_key: str
    image_id: int


class CommitImageRequest(BaseSchema):
    image_id: int


class CommitImageResponse(BaseSchema):
    image_url: str


class ImageCreate(BaseSchema):
    mime_type: str
    size_bytes: int
    file_key: str


class ImageUpdate(BaseSchema):
    status: AssetStatus
