from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from definition import Definition
    from category import Category
    from meaning import Meaning


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    meaning_id: Mapped[int] = mapped_column(
        ForeignKey("meanings.id", ondelete="SET NULL"), nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )

    @property
    def definition_ids(self) -> list[int]:
        return [d.id for d in self.definitions]

    is_correct: Mapped[bool] = mapped_column(
        default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    meaning: Mapped[Meaning | None] = relationship(
        "Meaning", back_populates="questions", lazy="joined"
    )
    category: Mapped[Category | None] = relationship(
        "Category", back_populates="questions", lazy="joined"
    )
    definitions: Mapped[list["Definition"]] = relationship(
        "Definition", back_populates="questions", secondary="definitions_questions"
    )
