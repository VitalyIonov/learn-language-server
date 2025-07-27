import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class AuthProvider(enum.Enum):
    GOOGLE = "google"
    EMAIL = "email"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    auth_provider: Mapped[AuthProvider] = mapped_column(
        default="google", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
