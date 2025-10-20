from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Issue
from app.schemas.client.issue import IssueCreate


async def create_issue(db: AsyncSession, new_issue: IssueCreate) -> Issue:
    entity = Issue(**new_issue.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


async def get_issues(db: AsyncSession, user_id: int) -> Sequence[Issue]:
    statement = (
        select(Issue)
        .where(Issue.reporter_id == user_id)
        .order_by(Issue.created_at.desc())
    )

    result = await db.execute(statement)
    orm_items = result.scalars().all()

    return orm_items
