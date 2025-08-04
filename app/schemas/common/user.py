from pydantic import EmailStr
from typing import List
from .common import BaseSchema


class UserOut(BaseSchema):
    id: int
    email: EmailStr
    name: str | None = None
    role: str

    class Config:
        from_attributes = True


class UserCreate(BaseSchema):
    email: EmailStr
    name: str | None = None


class UsersListResponse(BaseSchema):
    items: List[UserOut]
