from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import QuestionType
from app.schemas.admin import QuestionTypeListResponse


async def get_question_types(db: AsyncSession) -> QuestionTypeListResponse:
    stmt = select(QuestionType).order_by(QuestionType.name)

    result = await db.execute(stmt)

    return QuestionTypeListResponse.model_validate({"items": result.scalars().all()})
