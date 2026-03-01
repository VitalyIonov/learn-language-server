from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from .question_type import QuestionTypeName

if TYPE_CHECKING:
    from .definition import Definition
    from .category import Category
    from .meaning import Meaning
    from .level import Level


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[QuestionTypeName] = mapped_column(
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meanings.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="SET NULL"), nullable=True)
    correct_definition_id: Mapped[int] = mapped_column(ForeignKey("definitions.id", ondelete="SET NULL"), nullable=True)
    chosen_definition_id: Mapped[int] = mapped_column(ForeignKey("definitions.id", ondelete="SET NULL"), nullable=True)

    @property
    def definition_ids(self) -> list[int]:
        return [d.id for d in self.definitions]

    is_correct: Mapped[bool] = mapped_column(nullable=True)
    score_delta: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    level: Mapped[Level | None] = relationship("Level", lazy="selectin")
    meaning: Mapped[Meaning | None] = relationship("Meaning", lazy="selectin")
    category: Mapped[Category | None] = relationship("Category", lazy="selectin", back_populates="questions")
    correct_definition: Mapped["Definition | None"] = relationship(
        "Definition",
        foreign_keys=[correct_definition_id],
        lazy="selectin",
    )
    definitions: Mapped[list["Definition"]] = relationship("Definition", secondary="definitions_questions")
