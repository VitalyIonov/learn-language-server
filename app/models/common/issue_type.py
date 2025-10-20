from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class IssueType(Base):
    __tablename__ = "issue_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
