from typing import List, Optional

from app.constants.issue_status import IssueStatusName
from app.constants.issue_type import IssueTypeName
from app.schemas.base import BaseSchema


class IssueOut(BaseSchema):
    id: int
    text: Optional[str] = None
    decision: Optional[str] = None
    status: IssueStatusName
    type: IssueTypeName
    meaning: str
    definitions: List[str]

    class Config:
        from_attributes = True


class IssueCreate(BaseSchema):
    text: Optional[str] = None
    type: IssueTypeName
    status: Optional[IssueStatusName] = None
    reporter_id: Optional[int] = None
    question_id: int
    meaning: str
    definitions: List[str]


class IssueUpdate(BaseSchema):
    text: str


class IssuesListResponse(BaseSchema):
    items: List[IssueOut]
