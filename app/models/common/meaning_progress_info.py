from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Meaning, Level


class MeaningProgressInfo(Base):
    __tablename__ = "meanings_progress_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meanings.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    score: Mapped[int] = mapped_column(default=0, server_default="0")

    meaning: Mapped["Meaning"] = relationship("Meaning")
    level: Mapped[Level | None] = relationship(
        "Level",
        foreign_keys=lambda: [MeaningProgressInfo.level_id],
    )
