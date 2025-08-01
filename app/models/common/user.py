import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class AuthProvider(enum.Enum):
    GOOGLE = "google"
    EMAIL = "email"


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=True)
    auth_provider: Mapped[AuthProvider] = mapped_column(
        default=AuthProvider.GOOGLE, nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        default=UserRole.USER,
        server_default=sa.text(f"'{UserRole.USER.name}'"),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
