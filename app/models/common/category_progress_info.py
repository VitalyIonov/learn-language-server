from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Category, Level


class CategoryProgressInfo(Base):
    __tablename__ = "categories_progress_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column(default=0, server_default="0")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    current_level_id: Mapped[int] = mapped_column(
        ForeignKey("levels.id", ondelete="SET NULL"), nullable=True
    )

    category: Mapped["Category"] = relationship(
        "Category", back_populates="categories_progress_info", lazy="joined"
    )
    current_level: Mapped[Level | None] = relationship("Level", lazy="joined")
