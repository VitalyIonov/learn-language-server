from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.models.level import Level
from app.models.meaning import Meaning
from app.models.definition import Definition


async def seed_definitions(session: AsyncSession, data: list[dict]) -> None:
    async with session.begin():
        for item in data:
            exists = await session.execute(
                select(Definition).where(Definition.text == item["text"])
            )
            if exists.scalars().first():
                continue

            category_id = await session.scalar(
                select(Category.id).where(Category.name == item["category"])
            )
            level_id = await session.scalar(
                select(Level.id).where(Level.alias == item["level"])
            )
            meaning_objs = (
                await session.scalars(
                    select(Meaning).where(Meaning.name.in_(item["meanings"]))
                )
            ).all()

            definition = Definition(
                text=item["text"],
                category_id=category_id,
                level_id=level_id,
            )

            definition.meanings.extend(meaning_objs)

            session.add(definition)
