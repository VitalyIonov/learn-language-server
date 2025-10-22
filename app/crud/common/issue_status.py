from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import IssueStatus
from app.schemas.common import IssueStatusListResponse


async def get_issue_status(
    db: AsyncSession,
    issue_status_id: int,
) -> IssueStatus | None:
    statement = select(IssueStatus).where(IssueStatus.id == issue_status_id)

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def get_issue_status_by_value(
    db: AsyncSession,
    issue_status_value: int,
) -> IssueStatus | None:
    statement = select(IssueStatus).where(IssueStatus.value == issue_status_value)

    result = await db.execute(statement)

    return result.scalar_one_or_none()


async def get_issue_statuses(
    db: AsyncSession,
) -> IssueStatusListResponse:
    statement = select(IssueStatus).order_by(IssueStatus.value)

    result = await db.execute(statement)

    return IssueStatusListResponse.model_validate(
        {
            "items": result.scalars().all(),
        }
    )
