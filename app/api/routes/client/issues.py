from fastapi import APIRouter, Depends

from app.core.dependencies.client import get_issue_service
from app.core.dependencies.common import get_current_user
from app.schemas.client.issue import IssueOut, IssueCreate, IssuesListResponse
from app.schemas.common import UserOut
from app.services.client import IssueService

router = APIRouter(tags=["issues"])


@router.post("/issues", response_model=IssueOut)
async def add_issue(
    new_issue: IssueCreate,
    current_user: UserOut = Depends(get_current_user),
    svc: IssueService = Depends(get_issue_service),
):
    return await svc.create(new_issue, current_user.id)


@router.get("/issues", response_model=IssuesListResponse)
async def get_issue(
    current_user: UserOut = Depends(get_current_user),
    svc: IssueService = Depends(get_issue_service),
):
    return await svc.get_all(current_user.id)
