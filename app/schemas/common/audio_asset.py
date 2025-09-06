from app.models import AssetStatus
from app.schemas.common import BaseSchema


class AudioAssetOut(BaseSchema):
    id: int
    status: AssetStatus
    mime_type: str
    size_bytes: int
    alt: str
    width: int | None = None
    height: int | None = None
    file_key: str
    url: str

    class Config:
        from_attributes = True


class AudioAssetUpload(BaseSchema):
    content_type: str
    size_bytes: int


class AudioAssetUploadOut(BaseSchema):
    upload_url: str
    file_key: str
    audio_id: int


class AudioAssetCreate(BaseSchema):
    mime_type: str
    size_bytes: int
    file_key: str


class AudioAssetUpdate(BaseSchema):
    status: AssetStatus


class AudioAssetCommit(BaseSchema):
    audio_id: int


class AudioAssetCommitOut(BaseSchema):
    audio_url: str
