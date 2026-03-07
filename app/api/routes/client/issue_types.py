from fastapi import APIRouter

from app.constants.issue_type import IssueTypeName
from app.schemas.common import IssueTypeListResponse
from app.schemas.common.issue_type import IssueTypeOut

router = APIRouter(tags=["issue_types"])


@router.get(
    "/issue_types",
    response_model=IssueTypeListResponse,
    operation_id="getIssueTypesList",
)
async def get_issue_types():
    return IssueTypeListResponse(
        items=[IssueTypeOut(name=issue_type) for issue_type in IssueTypeName]
    )
