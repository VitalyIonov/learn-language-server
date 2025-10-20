from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.common import get_issue_types as get_issue_types_crud


class IssueTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        return await get_issue_types_crud(self.db)
