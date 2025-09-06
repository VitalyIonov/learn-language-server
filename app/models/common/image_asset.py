from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .asset import Asset, AssetType


class ImageAsset(Asset):
    __tablename__ = "image_assets"
    id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True
    )
    alt: Mapped[str] = mapped_column(String(100), nullable=False)
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)

    __mapper_args__ = {"polymorphic_identity": AssetType.IMAGE.value}
