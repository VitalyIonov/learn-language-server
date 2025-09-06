from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .definition import Definition
from .image_asset import ImageAsset


class ImageDefinition(Definition):
    __tablename__ = "image_definitions"
    id: Mapped[int] = mapped_column(
        ForeignKey("definitions.id", ondelete="CASCADE"), primary_key=True
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )

    image: Mapped[ImageAsset] = relationship("Asset", lazy="selectin")
    __mapper_args__ = {"polymorphic_identity": "image"}
