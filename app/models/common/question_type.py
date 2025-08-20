from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class QuestionType(Base):
    __tablename__ = "question_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
