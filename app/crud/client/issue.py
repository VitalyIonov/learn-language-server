from fastapi import HTTPException
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.models import Issue, IssueStatus
from app.schemas.client.issue import IssueCreate

MAX_ISSUES_COUNT = 50
NEW_ISSUE_STATUS_VALUE = 0


async def create_issue(db: AsyncSession, new_issue: IssueCreate) -> Issue | None:
    count_statement = select(count(Issue.id)).where(
        Issue.reporter_id == new_issue.reporter_id,
        IssueStatus.value == NEW_ISSUE_STATUS_VALUE,
    )

    issues_count = await db.scalar(count_statement) or 0

    if issues_count >= MAX_ISSUES_COUNT:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Слишком много обращений. Дождитесь обработки предыдущих.",
            headers={"Retry-After": "3600"},
        )

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
