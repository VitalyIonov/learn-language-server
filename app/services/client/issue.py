from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.issue_status import INITIAL_ISSUE_STATUS
from app.crud.client import (
    create_issue as create_issue_crud,
    get_issues as get_issues_crud,
)
from app.models import Issue
from app.schemas.client import IssueCreate


class IssueService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: IssueCreate, user_id: int):
        updates: dict = {
            "reporter_id": user_id,
            "status": INITIAL_ISSUE_STATUS,
        }

        new_payload = payload.model_copy(update=updates)

        return await create_issue_crud(self.db, new_payload)

    async def get_all(self, user_id: int) -> Sequence[Issue]:
        return await get_issues_crud(self.db, user_id)
