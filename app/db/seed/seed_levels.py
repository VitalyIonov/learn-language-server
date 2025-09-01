from sqlalchemy import select

from app.models import QuestionType, Level
from sqlalchemy.ext.asyncio import AsyncSession


async def seed_levels(session: AsyncSession, data: list[dict]):
    async with session.begin():
        for item in data:
            result = await session.execute(
                select(Level).where(Level.alias == item["alias"])
            )
            if result.scalars().first():
                continue

            question_type_objs = (
                await session.scalars(
                    select(QuestionType).where(
                        QuestionType.name.in_(item["question_types"])
                    )
                )
            ).all()

            level = Level(
                name=item["name"],
                alias=item["alias"],
                value=item["value"],
            )

            level.question_types.extend(question_type_objs)

            session.add(level)
