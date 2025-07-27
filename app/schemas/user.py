from pydantic import EmailStr
from typing import List
from app.schemas import NonNegativeInt, BaseSchema


class UserOut(BaseSchema):
    id: NonNegativeInt
    email: EmailStr
    name: str | None = None

    class Config:
        from_attributes = True


class UsersListResponse(BaseSchema):
    items: List[UserOut]
