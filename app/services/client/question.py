import random

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import load_only

from app.schemas.admin import CategoryProgressInfoCreate
from app.services.admin import CategoryProgressInfoService
from app.schemas.client import QuestionOut
from app.models import User, Meaning, Level, Definition


class QuestionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate(
        self, category_id: int, level_id: int, current_user: User
    ) -> QuestionOut:
        category_progress_info_svc = CategoryProgressInfoService(self.db)

        category_progress_info = await category_progress_info_svc.get(
            current_user.id, category_id
        )

        if category_progress_info is None:
            category_progress_info = await category_progress_info_svc.create(
                CategoryProgressInfoCreate(
                    user_id=current_user.id,
                    category_id=category_id,
                    current_level_id=level_id,
                )
            )

        current_level_value = category_progress_info.current_level.value
        meaning_stmt = (
            select(Meaning)
            .join(Meaning.level)
            .options(load_only(Meaning.id, Meaning.name))
            .where(
                Meaning.definitions.any(),
                Meaning.category_id == category_id,
                Level.value == current_level_value,
            )
            .order_by(func.random())
            .limit(1)
        )
        meaning = await self.db.scalar(meaning_stmt)

        definition_false_stmt = (
            select(Definition)
            .join(Definition.level)
            .options(load_only(Definition.id, Definition.text))
            .where(
                Level.value == current_level_value,
                ~Definition.meanings.any(Meaning.id == meaning.id),
            )
            .order_by(func.random())
            .limit(2)
        )

        definition_true_stmt = (
            select(Definition)
            .join(Definition.level)
            .options(load_only(Definition.id, Definition.text))
            .where(
                Level.value == current_level_value,
                Definition.meanings.any(Meaning.id == meaning.id),
            )
            .order_by(func.random())
            .limit(1)
        )

        false_definitions = list(
            (await self.db.execute(definition_false_stmt)).scalars().all()
        )
        true_definitions = list(
            (await self.db.execute(definition_true_stmt)).scalars().all()
        )

        definitions = false_definitions + true_definitions
        random.shuffle(definitions)

        return QuestionOut.model_validate(
            {
                "meaning": meaning,
                "definitions": definitions,
            }
        )
