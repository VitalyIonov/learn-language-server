from fastapi import APIRouter, Depends

from app.core.dependencies.service_factories import (
    get_current_user,
    get_issue_service_client,
)
from app.schemas.client.issue import IssueOut, IssueCreate, IssuesListResponse
from app.schemas.common import UserOut
from app.services.client import IssueService

router = APIRouter(tags=["issues"])


@router.post("/issues", response_model=IssueOut, operation_id="createIssue")
async def add_issue(
    new_issue: IssueCreate,
    current_user: UserOut = Depends(get_current_user),
    svc: IssueService = Depends(get_issue_service_client),
):
    return await svc.create(new_issue, current_user.id)


@router.get("/issues", response_model=IssuesListResponse, operation_id="getIssuesList")
async def get_issue(
    current_user: UserOut = Depends(get_current_user),
    svc: IssueService = Depends(get_issue_service_client),
):
    return await svc.get_all(current_user.id)
