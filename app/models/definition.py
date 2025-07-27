from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from app.models.associations import definitions_meanings

if TYPE_CHECKING:
    from category import Category
    from level import Level
    from meaning import Meaning


class Definition(Base):
    __tablename__ = "definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(index=True, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
    )
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id"),
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
        secondary=definitions_meanings,
    )
