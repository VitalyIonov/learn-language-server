from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Definition, QuestionTypeName
from app.models.common import Question
from app.models.common.associations import DefinitionsMeanings
from app.models.common.definition_progress_info import DefinitionProgressInfo
from app.schemas.client import QuestionCreate, QuestionUpdate
from app.schemas.client.question import DefinitionCandidate


async def get_definition_candidates(
    db: AsyncSession,
    level_id: int,
    category_id: int,
    user_id: int,
) -> list[DefinitionCandidate]:
    stmt = (
        select(
            Definition.id,
            DefinitionsMeanings.meaning_id,
            Definition.group,
            Definition.type,
            func.coalesce(DefinitionProgressInfo.chance, 100.0).label("chance"),
        )
        .join(
            DefinitionsMeanings,
            DefinitionsMeanings.definition_id == Definition.id,
        )
        .outerjoin(
            DefinitionProgressInfo,
            (DefinitionProgressInfo.definition_id == Definition.id)
            & (DefinitionProgressInfo.meaning_id == DefinitionsMeanings.meaning_id)
            & (DefinitionProgressInfo.user_id == user_id),
        )
        .where(
            Definition.level_id == level_id,
            Definition.category_id == category_id,
        )
    )

    result = await db.execute(stmt)
    return [DefinitionCandidate(*row) for row in result.all()]


async def get_definitions_by_ids(
    db: AsyncSession,
    definition_ids: list[int],
) -> list[Definition]:
    stmt = select(Definition).where(Definition.id.in_(definition_ids))
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_question(db: AsyncSession, question_id: int) -> Question | None:
    entity = await db.get(Question, question_id)
    return entity


async def create_question(
    db: AsyncSession, new_question: QuestionCreate, definition_ids: list[int]
) -> Question:
    definitions: Sequence[Definition] = []

    if definition_ids:
        definitions = (
            (
                await db.execute(
                    select(Definition).where(Definition.id.in_(definition_ids))
                )
            )
            .scalars()
            .all()
        )

    entity = Question(**new_question.model_dump())
    entity.definitions = list(definitions)
    db.add(entity)
    await db.flush()

    await db.commit()
    await db.refresh(entity)
    return entity


async def update_question(
    db: AsyncSession, db_item: Question, item_update: QuestionUpdate
) -> Question:
    is_correct = item_update.chosen_definition_id == db_item.correct_definition_id
    payload = item_update.model_dump()
    payload["is_correct"] = is_correct

    for field, value in payload.items():
        setattr(db_item, field, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item
