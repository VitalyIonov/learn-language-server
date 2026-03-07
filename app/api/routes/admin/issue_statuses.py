from fastapi import APIRouter

from app.constants.issue_status import IssueStatusName
from app.schemas.common import IssueStatusListResponse
from app.schemas.common.issue_status import IssueStatusOut

router = APIRouter(tags=["issue_statuses"])


@router.get("/issue_statuses", response_model=IssueStatusListResponse)
async def get_issue_statuses():
    return IssueStatusListResponse(
        items=[
            IssueStatusOut(name=issue_status) for issue_status in IssueStatusName
        ]
    )
