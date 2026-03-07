from app.constants.issue_type import IssueTypeName
from app.schemas.base import BaseSchema


class IssueTypeOut(BaseSchema):
    name: IssueTypeName


class IssueTypeListResponse(BaseSchema):
    items: list[IssueTypeOut]
