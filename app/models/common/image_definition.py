from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .definition import Definition


class ImageDefinition(Definition):
    __tablename__ = "image_definitions"
    id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"))

    __mapper_args__ = {"polymorphic_identity": "image"}
