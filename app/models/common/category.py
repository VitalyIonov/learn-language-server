from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from .definition import Definition
    from .meaning import Meaning
    from .question import Question
    from .asset import Asset


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    image_id: Mapped[int | None] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL")
    )

    image: Mapped[Asset | None] = relationship("Asset", lazy="selectin")
    meanings: Mapped[list[Meaning]] = relationship(
        "Meaning",
        back_populates="category",
    )
    definitions: Mapped[list["Definition"]] = relationship(
        "Definition",
        back_populates="category",
    )
    questions: Mapped[list[Question]] = relationship(
        "Question",
        back_populates="category",
    )
