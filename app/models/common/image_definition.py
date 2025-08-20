from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .definition import Definition
from .asset import Asset


class ImageDefinition(Definition):
    __tablename__ = "image_definitions"
    id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"))

    image: Mapped[Asset] = relationship("Asset", lazy="selectin")
    __mapper_args__ = {"polymorphic_identity": "image"}
