from fastapi import APIRouter, Depends, Query

from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.core.dependencies.service_factories import get_issue_service_admin
from app.schemas.admin.issue import IssueOut, IssueUpdate, IssuesListResponse
from app.services.admin import IssueService

router = APIRouter(tags=["issues"])


@router.get("/issues/{issue_id}", response_model=IssueOut)
async def get_issue(
    issue_id: int,
    svc: IssueService = Depends(get_issue_service_admin),
):
    return await svc.get(issue_id)


@router.get("/issues", response_model=IssuesListResponse)
async def get_issues(
    offset: int = Query(DEFAULT_OFFSET, description="offset"),
    limit: int = Query(DEFAULT_LIMIT, description="page size"),
    q: str = Query("", description="Search query"),
    svc: IssueService = Depends(get_issue_service_admin),
):
    return await svc.get_all(offset, limit, q)


@router.patch("/issues/{issue_id}", response_model=IssueOut)
async def update_issue(
    issue_id: int,
    payload: IssueUpdate,
    svc: IssueService = Depends(get_issue_service_admin),
):
    return await svc.update(issue_id, payload)
