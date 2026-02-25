from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Meaning, Level, Category


class MeaningProgressInfo(Base):
    __tablename__ = "meanings_progress_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meanings.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(default=0, server_default="0")

    meaning: Mapped["Meaning"] = relationship("Meaning", lazy="raise")
    level: Mapped["Level"] = relationship("Level", lazy="raise")
    category: Mapped["Category"] = relationship("Category", lazy="raise")
