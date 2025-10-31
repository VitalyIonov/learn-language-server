from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Translation(Base):
    __tablename__ = "translations"
    __table_args__ = (
        UniqueConstraint(
            "text", "lang_from", "lang_to", name="uq_translations_text_langs"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(index=True, nullable=False)
    translated_text: Mapped[str] = mapped_column(nullable=False)
    lang_from: Mapped[str] = mapped_column(index=True, nullable=False)
    lang_to: Mapped[str] = mapped_column(index=True, nullable=False)
