from datetime import datetime
from app.schemas.common import BaseSchema
from app.models.common.asset import AssetStatus


class AssetOut(BaseSchema):
    id: int
    status: AssetStatus
    mime_type: str
    size_bytes: int
    width: int | None = None
    height: int | None = None
    file_key: str
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
