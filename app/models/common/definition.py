from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from .question_type import QuestionTypeName

if TYPE_CHECKING:
    from .category import Category
    from .level import Level
    from .meaning import Meaning
    from .question import Question


class Definition(Base):
    __tablename__ = "definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[QuestionTypeName] = mapped_column(
        nullable=False,
        index=True,
    )
    text: Mapped[str] = mapped_column(nullable=False, index=True, server_default="")

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
        secondary="definitions_meanings",
        lazy="selectin",
    )
    questions: Mapped[list[Question]] = relationship(
        "Question",
        back_populates="definitions",
        secondary="definitions_questions",
    )

    __mapper_args__ = {
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }
