from typing import List, Optional

from app.schemas.base import BaseSchema
from app.schemas.common import IssueTypeOut, IssueStatusOut


class IssueOut(BaseSchema):
    id: int
    text: Optional[str] = None
    decision: Optional[str] = None
    status: Optional[IssueStatusOut] = None
    type: Optional[IssueTypeOut] = None
    meaning: str
    definitions: List[str]

    class Config:
        from_attributes = True


class IssueCreate(BaseSchema):
    text: Optional[str] = None
    type_id: int
    status_id: Optional[int] = None
    reporter_id: Optional[int] = None
    question_id: int
    meaning: str
    definitions: List[str]


class IssueUpdate(BaseSchema):
    text: str


class IssuesListResponse(BaseSchema):
    items: List[IssueOut]
