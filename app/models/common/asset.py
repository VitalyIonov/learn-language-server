import enum
from datetime import datetime

from sqlalchemy import String, func, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.utils.url_generator import public_url


class AssetStatus(enum.Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"


class AssetType(str, enum.Enum):
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, native_enum=False),
        nullable=False,
        server_default=AssetType.IMAGE,
        index=True,
    )
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus, native_enum=False),
        nullable=False,
        server_default=AssetStatus.PENDING.value,
    )
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    file_key: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @hybrid_property
    def url(self) -> str:
        return public_url(self.file_key)

    __mapper_args__ = {
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }
