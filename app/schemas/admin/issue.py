from typing import List, Optional

from app.schemas.base import BaseSchema
from app.schemas.common import IssueTypeOut, IssueStatusOut, UserOut, Meta
from app.schemas.admin import QuestionOut


class IssueOut(BaseSchema):
    id: int
    text: str
    reporter: Optional[UserOut] = None
    status: Optional[IssueStatusOut] = None
    type: Optional[IssueTypeOut] = None
    question: Optional[QuestionOut] = None
    meaning: str
    definitions: List[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class IssueUpdate(BaseSchema):
    text: str
    status_id: int


class IssuesListResponse(BaseSchema):
    items: List[IssueOut]
    meta: Meta
