from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from .associations import DefinitionsMeanings

if TYPE_CHECKING:
    from app.models.common.category import Category
    from .level import Level
    from .meaning import Meaning
    from .question import Question


class Definition(Base):
    __tablename__ = "definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(index=True, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    level_id: Mapped[int] = mapped_column(
        ForeignKey(
            "levels.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    @property
    def meaning_ids(self) -> list[int]:
        return [m.id for m in self.meanings]

    category: Mapped[Category | None] = relationship(
        "Category",
        back_populates="definitions",
        lazy="selectin",
    )
    level: Mapped[Level | None] = relationship(
        "Level",
        lazy="selectin",
    )
    meanings: Mapped[list[Meaning]] = relationship(
        "Meaning",
        back_populates="definitions",
        secondary=DefinitionsMeanings.__tablename__,
        lazy="selectin",
    )
    questions: Mapped[list[Question]] = relationship(
        "Question",
        back_populates="definitions",
        secondary="definitions_questions",
    )
