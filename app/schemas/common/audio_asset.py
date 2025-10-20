from app.models import AssetStatus
from app.schemas.base import BaseSchema


class AudioAssetOut(BaseSchema):
    id: int
    status: AssetStatus
    mime_type: str
    size_bytes: int
    file_key: str
    url: str

    class Config:
        from_attributes = True


class AudioAssetUpload(BaseSchema):
    text: str


class AudioAssetUploadOut(BaseSchema):
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
