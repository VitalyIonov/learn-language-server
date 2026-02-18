from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from .question_type import QuestionTypeName
from app.constants.language import LanguageCode

if TYPE_CHECKING:
    from .category import Category
    from .level import Level
    from .meaning import Meaning


class Definition(Base):
    __tablename__ = "definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[QuestionTypeName] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False, index=True)

    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)
    language: Mapped[LanguageCode | None] = mapped_column(nullable=True, server_default=LanguageCode.ES.value)

    category: Mapped[Category | None] = relationship("Category", back_populates="definitions", lazy="raise")
    level: Mapped[Level | None] = relationship("Level", lazy="raise")
    meanings: Mapped[list[Meaning]] = relationship("Meaning", back_populates="definitions", secondary="definitions_meanings", lazy="raise")

    @property
    def meaning_ids(self) -> list[int]:
        return [m.id for m in self.meanings]

    __mapper_args__ = {
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }
