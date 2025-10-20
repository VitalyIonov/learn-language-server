from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class IssueStatus(Base):
    __tablename__ = "issue_statuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    value: Mapped[int] = mapped_column(unique=True, nullable=False)
