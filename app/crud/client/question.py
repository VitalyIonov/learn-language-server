from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Definition
from app.models.common import Question
from app.schemas.client import QuestionCreate, QuestionUpdate, QuestionUpdateOut


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
