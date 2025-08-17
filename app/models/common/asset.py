import enum
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.utils.url_generator import public_url


class AssetStatus(enum.Enum):
    PENDING = "pending"
    READY = "ready"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[AssetStatus] = mapped_column(
        default=AssetStatus.PENDING, nullable=False
    )
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    width: Mapped[int | None]
    height: Mapped[int | None]
    file_key: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @hybrid_property
    def image_url(self) -> str:
        return public_url(self.file_key)
