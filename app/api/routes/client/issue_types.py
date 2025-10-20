from fastapi import APIRouter, Depends

from app.core.dependencies.common import get_issue_type_service
from app.schemas.common import IssueTypeListResponse
from app.services.common import IssueTypeService

router = APIRouter(tags=["issue_types"])


@router.get("/issue_types", response_model=IssueTypeListResponse)
async def get_issue_types(
    svc: IssueTypeService = Depends(get_issue_type_service),
):
    return await svc.get_all()
