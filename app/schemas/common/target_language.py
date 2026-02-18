from app.schemas.base import BaseSchema


class TargetLanguageOut(BaseSchema):
    code: str
    display_name: str


class TargetLanguageListResponse(BaseSchema):
    items: list[TargetLanguageOut]
