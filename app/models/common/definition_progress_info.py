from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.common import Meaning, Definition, Level, Category


class DefinitionProgressInfo(Base):
    __tablename__ = "definitions_progress_info"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    meaning_id: Mapped[int] = mapped_column(ForeignKey("meanings.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    definition_id: Mapped[int] = mapped_column(ForeignKey("definitions.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chance: Mapped[int] = mapped_column(default=100, server_default="100")

    meaning: Mapped["Meaning"] = relationship("Meaning", lazy="raise")
    definition: Mapped["Definition"] = relationship("Definition", lazy="raise")
    level: Mapped["Level"] = relationship("Level", lazy="raise")
    category: Mapped["Category"] = relationship("Category", lazy="raise")
