from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.client import (
    create_issue as create_issue_crud,
    get_issues as get_issues_crud,
)
from app.models import Issue
from app.schemas.client import IssueCreate

from ..common.issue_status import IssueStatusService

INITIAL_ISSUE_STATUS_VALUE = 0


class IssueService:
    def __init__(self, db: AsyncSession, svc_issue_status: IssueStatusService):
        self.db = db
        self.svc_issue_status = svc_issue_status

    async def create(self, payload: IssueCreate, user_id: int):
        updates: dict = {"reporter_id": user_id}
        new_status = await self.svc_issue_status.get_by_value(
            INITIAL_ISSUE_STATUS_VALUE
        )

        if new_status:
            updates["status_id"] = new_status.id

        new_payload = payload.model_copy(update=updates)

        return await create_issue_crud(self.db, new_payload)

    async def get_all(self, user_id: int) -> Sequence[Issue]:
        return await get_issues_crud(self.db, user_id)
