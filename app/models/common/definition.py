from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from .associations import DefinitionsMeanings

if TYPE_CHECKING:
    from app.models.common.category import Category
    from level import Level
    from meaning import Meaning
    from question import Question
    from definition_progress_info import DefinitionProgressInfo


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
        lazy="joined",
    )
    level: Mapped[Level | None] = relationship(
        "Level",
        back_populates="definitions",
        lazy="joined",
    )
    meanings: Mapped[list[Meaning]] = relationship(
        "Meaning",
        back_populates="definitions",
        secondary=DefinitionsMeanings.__tablename__,
    )
    questions: Mapped[list[Question]] = relationship(
        "Question",
        back_populates="definitions",
        secondary="definitions_questions",
    )
    definitions_progress_info: Mapped[list[DefinitionProgressInfo]] = relationship(
        "DefinitionProgressInfo",
        back_populates="definition",
        lazy="joined",
    )
