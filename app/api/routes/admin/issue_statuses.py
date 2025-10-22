from fastapi import APIRouter, Depends

from app.core.dependencies.common import get_issue_status_service
from app.schemas.common import IssueStatusListResponse
from app.services.common import IssueTypeService

router = APIRouter(tags=["issue_statuses"])


@router.get("/issue_statuses", response_model=IssueStatusListResponse)
async def get_issue_statuses(
    svc: IssueTypeService = Depends(get_issue_status_service),
):
    return await svc.get_all()
