from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .asset import Asset, AssetType


class AudioAsset(Asset):
    __tablename__ = "audio_assets"
    id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True
    )

    __mapper_args__ = {"polymorphic_identity": AssetType.AUDIO}
