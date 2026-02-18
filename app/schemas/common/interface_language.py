from app.constants.interface_language import InterfaceLanguageCode
from app.schemas.base import BaseSchema


class InterfaceLanguageOut(BaseSchema):
    code: InterfaceLanguageCode
    display_name: str


class InterfaceLanguageListResponse(BaseSchema):
    items: list[InterfaceLanguageOut]
