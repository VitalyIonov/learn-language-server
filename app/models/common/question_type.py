from __future__ import annotations

import enum

from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class QuestionTypeName(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"


class QuestionType(Base):
    __tablename__ = "question_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[QuestionTypeName] = mapped_column(index=True, nullable=False)
