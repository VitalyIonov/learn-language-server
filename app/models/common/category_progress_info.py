from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Category, Level


class CategoryProgressInfo(Base):
    __tablename__ = "categories_progress_info"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id", ondelete="CASCADE"), nullable=False, primary_key=True
    )
    score: Mapped[int] = mapped_column(default=0, server_default="0")

    @property
    def level_value(self) -> int:
        return self.level.value

    category: Mapped["Category"] = relationship("Category")
    level: Mapped[Level] = relationship("Level", lazy="selectin")
