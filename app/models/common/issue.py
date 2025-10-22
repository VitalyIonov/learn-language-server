from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from .question import Question
    from .issue_type import IssueType
    from .issue_status import IssueStatus
    from .user import User


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    reporter_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL"), nullable=True
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey("issue_statuses.id", ondelete="SET NULL"), nullable=True
    )
    type_id: Mapped[int] = mapped_column(
        ForeignKey("issue_types.id", ondelete="SET NULL"), nullable=True
    )
    text: Mapped[str] = mapped_column(nullable=True)
    decision: Mapped[str] = mapped_column(nullable=True)
    meaning: Mapped[str] = mapped_column(nullable=False)
    definitions: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, nullable=False
    )

    reporter: Mapped["User"] = relationship(
        "User", back_populates="issues", lazy="selectin"
    )
    question: Mapped["Question"] = relationship("Question", lazy="selectin")
    status: Mapped["IssueStatus"] = relationship("IssueStatus", lazy="selectin")
    type: Mapped["IssueType"] = relationship("IssueType", lazy="selectin")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
