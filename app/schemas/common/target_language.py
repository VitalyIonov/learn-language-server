from app.constants.target_language import TargetLanguageCode
from app.schemas.base import BaseSchema


class TargetLanguageOut(BaseSchema):
    code: TargetLanguageCode
    display_name: str


class TargetLanguageListResponse(BaseSchema):
    items: list[TargetLanguageOut]
