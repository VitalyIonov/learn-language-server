from pydantic import EmailStr
from app.schemas import NonNegativeInt, BaseSchema


class UserOut(BaseSchema):
    id: NonNegativeInt
    email: EmailStr
    name: str | None = None

    class Config:
        from_attributes = True
