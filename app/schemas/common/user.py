from pydantic import EmailStr
from typing import List
from app.schemas.common import Meta
from app.schemas.base import BaseSchema
from app.constants.interface_language import InterfaceLanguageCode
from app.constants.target_language import TargetLanguageCode
from app.models.common.user import UserRole


class UserOut(BaseSchema):
    id: int
    email: EmailStr
    name: str | None = None
    interface_lang: InterfaceLanguageCode
    target_language: TargetLanguageCode
    role: UserRole

    class Config:
        from_attributes = True


class UserCreate(BaseSchema):
    email: EmailStr
    name: str | None = None


class UsersListResponse(BaseSchema):
    items: List[UserOut]
    meta: Meta
