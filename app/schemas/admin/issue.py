from datetime import datetime
from typing import List, Optional

from app.schemas.base import BaseSchema
from app.schemas.common import IssueTypeOut, IssueStatusOut, UserOut, Meta
from app.schemas.admin import QuestionOut


class IssueOut(BaseSchema):
    id: int
    text: Optional[str] = None
    decision: Optional[str] = None
    reporter: Optional[UserOut] = None
    status: Optional[IssueStatusOut] = None
    type: Optional[IssueTypeOut] = None
    question: Optional[QuestionOut] = None
    meaning: str
    definitions: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IssueUpdate(BaseSchema):
    decision: Optional[str] = None
    status_id: Optional[int] = None


class IssuesListResponse(BaseSchema):
    items: List[IssueOut]
    meta: Meta
