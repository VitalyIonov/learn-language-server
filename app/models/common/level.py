from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

if TYPE_CHECKING:
    from meaning import Meaning
    from definition import Definition


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    alias: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    meanings: Mapped[list["Meaning"]] = relationship(
        "Meaning",
        back_populates="level",
    )

    definitions: Mapped[list["Definition"]] = relationship(
        "Definition",
        back_populates="level",
    )
