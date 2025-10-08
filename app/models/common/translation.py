from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(index=True, nullable=False)
    context: Mapped[str | None] = mapped_column(index=True, nullable=True)
    translated_text: Mapped[str] = mapped_column(nullable=False)
    lang_from: Mapped[str] = mapped_column(index=True, nullable=False)
    lang_to: Mapped[str] = mapped_column(index=True, nullable=False)
