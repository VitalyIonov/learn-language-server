from datetime import datetime
from typing import List, Optional

from app.constants.issue_status import IssueStatusName
from app.constants.issue_type import IssueTypeName
from app.schemas.base import BaseSchema
from app.schemas.common import UserOut, Meta
from app.schemas.admin import QuestionOut


class IssueOut(BaseSchema):
    id: int
    text: Optional[str] = None
    decision: Optional[str] = None
    reporter: Optional[UserOut] = None
    status: IssueStatusName
    type: IssueTypeName
    question: Optional[QuestionOut] = None
    meaning: str
    definitions: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IssueUpdate(BaseSchema):
    decision: Optional[str] = None
    status: Optional[IssueStatusName] = None


class IssuesListResponse(BaseSchema):
    items: List[IssueOut]
    meta: Meta
