from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import IssueType
from app.schemas.common import IssueTypeListResponse


async def get_issue_types(
    db: AsyncSession,
) -> IssueTypeListResponse:
    statement = select(IssueType).order_by(IssueType.name)

    result = await db.execute(statement)

    return IssueTypeListResponse.model_validate(
        {
            "items": result.scalars().all(),
        }
    )
