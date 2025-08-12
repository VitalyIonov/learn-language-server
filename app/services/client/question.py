import random
from typing import cast

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import load_only

from app.schemas.admin import (
    CategoryProgressInfoCreate,
    MeaningProgressInfoCreate,
    DefinitionProgressInfoCreate,
    CategoryProgressInfoUpdate,
    MeaningProgressInfoUpdate,
    DefinitionProgressInfoUpdate,
)
from app.core.dependencies.admin import (
    get_category_progress_info_service,
    get_meaning_progress_info_service,
    get_definition_progress_info_service,
)
from app.schemas.client import (
    QuestionOut,
    QuestionCreate,
    QuestionUpdate,
    QuestionGenerate,
    QuestionUpdateOut,
)
from app.models import User, Meaning, Definition, Question, CategoryProgressInfo, Level
from app.crud.client import (
    create_question as crud_create_question,
    get_question as crud_get_question,
    update_question as crud_update_question,
)


class QuestionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_progress_info_svc = get_category_progress_info_service(self.db)
        self.meaning_progress_info_svc = get_meaning_progress_info_service(self.db)
        self.definition_progress_info_svc = get_definition_progress_info_service(
            self.db
        )

    async def generate(
        self, payload: QuestionGenerate, current_user: User
    ) -> QuestionOut:
        cpi_max_level_id = None
        min_level_id = None

        if payload.level_id is None:
            cpi_max_level_stmt = (
                select(CategoryProgressInfo.level_id)
                .where(
                    CategoryProgressInfo.user_id == current_user.id,
                    CategoryProgressInfo.category_id == payload.category_id,
                )
                .order_by(CategoryProgressInfo.level.value.desc())
                .limit(1)
            )

            cpi_max_level_id = (await self.db.execute(cpi_max_level_stmt)).scalar()

        if cpi_max_level_id is None:
            level_stmt = select(Level.id).order_by(Level.value.asc()).limit(1)
            min_level_id = (await self.db.execute(level_stmt)).scalar()

            if min_level_id is None:
                raise NoResultFound("No levels configured")

        question_level_id = payload.level_id or cpi_max_level_id or min_level_id

        meaning_stmt = (
            select(Meaning)
            .options(load_only(Meaning.id, Meaning.name))
            .where(
                Meaning.definitions.any(Definition.level_id == question_level_id),
                Meaning.category_id == payload.category_id,
                Meaning.level_id == question_level_id,
            )
            .order_by(func.random())
            .limit(1)
        )
        meaning = await self.db.scalar(meaning_stmt)

        if meaning is None:
            raise NoResultFound("Meaning not found")

        definition_false_stmt = (
            select(Definition)
            .options(load_only(Definition.id, Definition.text))
            .where(
                Definition.level_id == question_level_id,
                ~Definition.meanings.any(Meaning.id == meaning.id),
            )
            .order_by(func.random())
            .limit(2)
        )

        definition_true_stmt = (
            select(Definition)
            .options(load_only(Definition.id, Definition.text))
            .where(
                Definition.level_id == question_level_id,
                Definition.meanings.any(Meaning.id == meaning.id),
            )
            .order_by(func.random())
            .limit(1)
        )

        false_definitions = list(
            (await self.db.execute(definition_false_stmt)).scalars().all()
        )
        true_definition = (await self.db.execute(definition_true_stmt)).scalar()

        if true_definition is None:
            raise NoResultFound("Definition not found")

        true_definitions = [true_definition]

        definitions = false_definitions + true_definitions
        random.shuffle(definitions)
        definition_ids = [d.id for d in definitions]

        question_data = QuestionCreate(
            user_id=current_user.id,
            meaning_id=cast(int, meaning.id),
            category_id=payload.category_id,
            level_id=question_level_id,
            correct_definition_id=cast(int, true_definition.id),
        )

        question = await crud_create_question(self.db, question_data, definition_ids)

        return QuestionOut.model_validate(
            {
                "id": question.id,
                "meaning": meaning,
                "definitions": definitions,
            }
        )

    async def get(self, question_id: int) -> Question:
        entity = await crud_get_question(self.db, question_id)

        if entity is None:
            raise NoResultFound("Question not found")

        return entity

    async def update(
        self, question_id: int, payload: QuestionUpdate, current_user: User
    ) -> QuestionUpdateOut:
        entity = await self.get(question_id)
        category_progress_info = await self.category_progress_info_svc.get(
            user_id=current_user.id,
            category_id=entity.category_id,
            level_id=entity.level_id,
        )
        meaning_progress_info = await self.meaning_progress_info_svc.get(
            user_id=current_user.id,
            meaning_id=entity.meaning_id,
            level_id=entity.level_id,
        )
        definition_progress_info = await self.definition_progress_info_svc.get(
            user_id=current_user.id,
            meaning_id=entity.meaning_id,
            definition_id=payload.chosen_definition_id,
        )

        if category_progress_info is None:
            category_progress_info = await self.category_progress_info_svc.create(
                CategoryProgressInfoCreate(
                    user_id=current_user.id,
                    category_id=entity.category_id,
                    level_id=entity.level_id,
                )
            )
        if meaning_progress_info is None:
            meaning_progress_info = await self.meaning_progress_info_svc.create(
                MeaningProgressInfoCreate(
                    user_id=current_user.id,
                    meaning_id=entity.meaning_id,
                    level_id=entity.level_id,
                )
            )
        if definition_progress_info is None:
            definition_progress_info = await self.definition_progress_info_svc.create(
                DefinitionProgressInfoCreate(
                    user_id=current_user.id,
                    meaning_id=entity.meaning_id,
                    definition_id=payload.chosen_definition_id,
                )
            )

        result = await crud_update_question(self.db, entity, payload)
        cpi_new_score = (
            category_progress_info.score + 2
            if result.is_correct
            else category_progress_info.score - 3
        )
        mpi_new_score = (
            meaning_progress_info.score + 2
            if result.is_correct
            else meaning_progress_info.score - 3
        )
        dpi_new_score = (
            definition_progress_info.score + 2
            if result.is_correct
            else definition_progress_info.score - 3
        )

        if cpi_new_score >= 0 and cpi_new_score != category_progress_info.score:
            await self.category_progress_info_svc.update(
                user_id=current_user.id,
                category_id=entity.category_id,
                level_id=entity.level_id,
                payload=CategoryProgressInfoUpdate(
                    score=cpi_new_score,
                ),
            )
        if mpi_new_score >= 0 and mpi_new_score != meaning_progress_info.score:
            await self.meaning_progress_info_svc.update(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                level_id=entity.level_id,
                payload=MeaningProgressInfoUpdate(
                    score=mpi_new_score,
                ),
            )
        if dpi_new_score >= 0 and dpi_new_score != definition_progress_info.score:
            await self.definition_progress_info_svc.update(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                definition_id=entity.correct_definition_id,
                payload=DefinitionProgressInfoUpdate(
                    score=dpi_new_score,
                ),
            )

        return QuestionUpdateOut(is_correct=result.is_correct)
