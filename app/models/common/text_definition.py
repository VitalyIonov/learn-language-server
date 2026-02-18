from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .definition import Definition
from .audio_asset import AudioAsset


class TextDefinition(Definition):
    __tablename__ = "text_definitions"

    id: Mapped[int] = mapped_column(ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True)

    audio_id: Mapped[int | None] = mapped_column(ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)

    audio: Mapped[AudioAsset] = relationship("Asset", lazy="raise")

    __mapper_args__ = {"polymorphic_identity": "text"}
