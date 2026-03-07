from app.constants.issue_status import IssueStatusName
from app.schemas.base import BaseSchema


class IssueStatusOut(BaseSchema):
    name: IssueStatusName


class IssueStatusListResponse(BaseSchema):
    items: list[IssueStatusOut]
