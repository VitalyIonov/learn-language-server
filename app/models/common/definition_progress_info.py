from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Meaning, Definition


class DefinitionProgressInfo(Base):
    __tablename__ = "definitions_progress_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column(default=0, server_default="0")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    meaning_id: Mapped[int] = mapped_column(
        ForeignKey("meanings.id", ondelete="SET NULL"), nullable=True
    )
    definition_id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), nullable=False
    )

    meaning: Mapped[Meaning | None] = relationship(
        "Meaning", back_populates="definitions_progress_info", lazy="joined"
    )
    definition: Mapped[Definition | None] = relationship(
        "Definition", back_populates="definitions_progress_info", lazy="joined"
    )
