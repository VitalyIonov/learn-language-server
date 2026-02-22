from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .definition import Definition
from .audio_asset import AudioAsset
from app.constants.definition_group import DefinitionGroup


class TextDefinition(Definition):
    __tablename__ = "text_definitions"

    id: Mapped[int] = mapped_column(ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True)

    audio_id: Mapped[int | None] = mapped_column(ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    group: Mapped[DefinitionGroup | None] = mapped_column(String, nullable=True, index=True)

    audio: Mapped[AudioAsset] = relationship("Asset", lazy="selectin")

    __mapper_args__ = {"polymorphic_identity": "text"}
