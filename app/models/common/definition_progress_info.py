from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Meaning, Definition


class DefinitionProgressInfo(Base):
    __tablename__ = "definitions_progress_info"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    meaning_id: Mapped[int] = mapped_column(
        ForeignKey("meanings.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    definition_id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    @property
    def level_id(self) -> int:
        return self.meaning.level_id

    score: Mapped[int] = mapped_column(default=0, server_default="0")

    meaning: Mapped[Meaning] = relationship("Meaning")
    definition: Mapped[Definition] = relationship("Definition")
