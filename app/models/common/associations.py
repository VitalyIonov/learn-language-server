from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class DefinitionsMeanings(Base):
    __tablename__ = "definitions_meanings"

    definition_id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    meaning_id: Mapped[int] = mapped_column(
        ForeignKey("meanings.id", ondelete="CASCADE"), primary_key=True
    )


class DefinitionsQuestions(Base):
    __tablename__ = "definitions_questions"

    definition_id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )
