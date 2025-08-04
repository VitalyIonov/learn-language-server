from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from definition import Definition
    from meaning import Meaning
    from question import Question
    from category_progress_info import CategoryProgressInfo


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

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
        lazy="joined",
    )

    categories_progress_info: Mapped[list[CategoryProgressInfo]] = relationship(
        "CategoryProgressInfo",
        back_populates="category",
        lazy="joined",
    )
