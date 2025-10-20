from sqlalchemy import select, insert
from app.models.common import IssueStatus
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_issue_statuses(session: AsyncSession, data: list[dict]):
    for item in data:
        result = await session.execute(
            select(IssueStatus.id).where(IssueStatus.name == item["name"])
        )
        issue_status_id = result.scalar()

        if issue_status_id is None:
            stmt = insert(IssueStatus).values(**item)
            await session.execute(stmt)

    await session.commit()
