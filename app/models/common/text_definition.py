from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .definition import Definition


class TextDefinition(Definition):
    __tablename__ = "text_definitions"
    id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    text: Mapped[str] = mapped_column(nullable=False, index=True)

    __mapper_args__ = {"polymorphic_identity": "text"}
