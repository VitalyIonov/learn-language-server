from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud.admin import (
    update_issue as update_issue_crud,
    get_issues as get_issues_crud,
    get_issue as get_issue_crud,
)
from app.models import Issue
from app.schemas.admin import IssueUpdate, IssuesListResponse


class IssueService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, issue_id: int) -> Issue | None:
        return await get_issue_crud(self.db, issue_id)

    async def update(self, issue_id: int, payload: IssueUpdate) -> Issue:
        entity = await self.get(issue_id)

        if entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
            )

        return await update_issue_crud(self.db, entity, payload)

    async def get_all(self, offset: int, limit: int, q: str) -> IssuesListResponse:
        return await get_issues_crud(self.db, offset, limit, q)
