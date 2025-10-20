from sqlalchemy import select, insert
from app.models.common import IssueType
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_issue_types(session: AsyncSession, data: list[dict]):
    for item in data:
        result = await session.execute(
            select(IssueType.id).where(IssueType.name == item["name"])
        )
        issue_type_id = result.scalar()

        if issue_type_id is None:
            stmt = insert(IssueType).values(**item)
            await session.execute(stmt)

    await session.commit()
