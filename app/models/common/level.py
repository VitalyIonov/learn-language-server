from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    alias: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    value: Mapped[float] = mapped_column(unique=True, nullable=False)
