from typing import Sequence, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT
from app.models import Issue
from app.schemas.admin.issue import IssueUpdate, IssuesListResponse


async def update_issue(
    db: AsyncSession, db_issue: Issue, payload: IssueUpdate
) -> Issue:
    update_data = payload.model_dump(exclude_unset=True)

    if update_data:
        for field, value in update_data.items():
            setattr(db_issue, field, value)

    await db.commit()
    await db.refresh(db_issue)
    return db_issue


async def get_issue(db: AsyncSession, issue_id: int) -> Issue | None:
    return await db.get(Issue, issue_id)


async def get_issues(
    db: AsyncSession,
    user_id: int,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> IssuesListResponse:
    statement = (
        select(Issue)
        .where(Issue.reporter_id == user_id)
        .order_by(Issue.created_at.desc())
    )
    count_statement = select(func.count()).select_from(Issue)

    if q:
        statement = statement.where(
            Issue.text.ilike(f"%{q}%"),
            Issue.meaning.ilike(f"%{q}%"),
            Issue.definitions.ilike(f"%{q}%"),
        )
        count_statement = count_statement.where(
            Issue.text.ilike(f"%{q}%"),
            Issue.meaning.ilike(f"%{q}%"),
            Issue.definitions.ilike(f"%{q}%"),
        )

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    total = (await db.execute(count_statement)).scalar_one()
    orm_items = result.scalars().all()

    return IssuesListResponse.model_validate(
        {"items": orm_items, "meta": {"total_count": total}}
    )
