from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from .definition import Definition

if TYPE_CHECKING:
    from .category import Category
    from .level import Level
    from .question import Question
    from .audio_asset import AudioAsset


class Meaning(Base):
    __tablename__ = "meanings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id", ondelete="SET NULL"),
        nullable=True,
    )
    audio_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )

    category: Mapped[Category] = relationship(
        "Category",
        back_populates="meanings",
        lazy="selectin",
    )
    level: Mapped[Level] = relationship("Level", lazy="selectin")
    audio: Mapped[AudioAsset] = relationship("Asset", lazy="selectin")
    definitions: Mapped[list[Definition]] = relationship(
        "Definition",
        secondary="definitions_meanings",
        back_populates="meanings",
        lazy="selectin",
    )
    questions: Mapped[list[Question]] = relationship(
        "Question", back_populates="meaning", lazy="selectin"
    )
