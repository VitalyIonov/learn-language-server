from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class UserInfo(Base):
    __tablename__ = "users_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    current_question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="SET NULL"), nullable=True
    )
