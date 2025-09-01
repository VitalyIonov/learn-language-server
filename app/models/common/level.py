from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from .question_type import QuestionType


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    alias: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    value: Mapped[int] = mapped_column(unique=True, nullable=False, server_default="0")

    @property
    def question_type_ids(self) -> list[int]:
        return [d.id for d in self.question_types]

    question_types: Mapped[list[QuestionType]] = relationship(
        "QuestionType",
        secondary="levels_question_types",
        lazy="selectin",
    )
