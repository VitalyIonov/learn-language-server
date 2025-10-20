from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.common import (
    get_issue_status as get_issue_status_crud,
    get_issue_status_by_value as get_issue_type_by_value_crud,
)


class IssueStatusService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, issue_status_id: int):
        return await get_issue_status_crud(self.db, issue_status_id)

    async def get_by_value(self, value: int):
        return await get_issue_type_by_value_crud(self.db, value)
