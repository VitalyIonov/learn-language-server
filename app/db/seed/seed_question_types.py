from sqlalchemy import select, insert
from app.models.common import QuestionType
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_question_types(session: AsyncSession, data: list[dict]):
    for question_type in data:
        result = await session.execute(
            select(QuestionType).where(QuestionType.name == question_type["name"])
        )
        if not result.scalar():
            stmt = insert(QuestionType).values(**question_type)
            await session.execute(stmt)
    await session.commit()
