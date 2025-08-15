import random
from typing import cast

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import load_only

from app.constants.score import BASE_SCORE
from app.schemas.admin import (
    CategoryProgressInfoUpdate,
    MeaningProgressInfoUpdate,
    DefinitionProgressInfoUpdate,
)

from app.schemas.client import (
    QuestionOut,
    QuestionCreate,
    QuestionUpdate,
    QuestionGenerate,
    QuestionUpdateOut,
    LevelUpInfo,
)
from app.models import User, Meaning, Definition, Question, Level, MeaningProgressInfo
from app.crud.client import (
    create_question as crud_create_question,
    get_question as crud_get_question,
    update_question as crud_update_question,
)
from app.services.admin import (
    CategoryProgressInfoService,
    MeaningProgressInfoService,
    DefinitionProgressInfoService,
)
from app.services.common import StatisticService


class QuestionService:
    def __init__(
        self,
        db: AsyncSession,
        svc_category_progress_info: CategoryProgressInfoService,
        svc_meaning_progress_info: MeaningProgressInfoService,
        svc_definition_progress_info: DefinitionProgressInfoService,
        svc_statistic: StatisticService,
    ):
        self.db = db
        self.svc_category_progress_info = svc_category_progress_info
        self.svc_meaning_progress_info = svc_meaning_progress_info
        self.svc_definition_progress_info = svc_definition_progress_info
        self.svc_statistic = svc_statistic

    async def generate(
        self, payload: QuestionGenerate, current_user: User
    ) -> QuestionOut:
        cpi_max_level_id = None
        min_level_id = None

        if payload.level_id is None:
            cpi_max_level_id = (
                await self.svc_category_progress_info.get_top_category_progress_info(
                    user_id=current_user.id, category_id=payload.category_id
                )
            ).level_id

        if cpi_max_level_id is None:
            level_stmt = select(Level.id).order_by(Level.value.asc()).limit(1)
            min_level_id = (await self.db.execute(level_stmt)).scalar()

            if min_level_id is None:
                raise NoResultFound("No levels configured")

        question_level_id = payload.level_id or cpi_max_level_id or min_level_id

        current_level_value_stmt = (
            select(Level.value).where(Level.id == question_level_id).scalar_subquery()
        )

        meaning_stmt = (
            select(Meaning)
            .join(Level, Meaning.level_id == Level.id)
            .options(load_only(Meaning.id, Meaning.name))
            .join(
                MeaningProgressInfo,
                and_(
                    MeaningProgressInfo.meaning_id == Meaning.id,
                    MeaningProgressInfo.level_id == question_level_id,
                    MeaningProgressInfo.user_id == current_user.id,
                ),
                isouter=True,
            )
            .where(
                Meaning.definitions.any(Definition.level_id == question_level_id),
                Meaning.category_id == payload.category_id,
                Level.value <= current_level_value_stmt,
                func.coalesce(MeaningProgressInfo.score, 0) < BASE_SCORE,
            )
            .order_by(func.random())
            .limit(1)
        )
        meaning = (await self.db.execute(meaning_stmt)).scalars().one_or_none()

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
        self,
        question_id: int,
        payload: QuestionUpdate,
        current_user: User,
    ) -> QuestionUpdateOut:
        entity = await self.get(question_id)
        category_progress_info = await self.svc_category_progress_info.get_or_create(
            user_id=current_user.id,
            category_id=entity.category_id,
            level_id=entity.level_id,
        )
        meaning_progress_info = await self.svc_meaning_progress_info.get_or_create(
            user_id=current_user.id,
            meaning_id=entity.meaning_id,
            level_id=entity.level_id,
        )
        definition_progress_info = (
            await self.svc_definition_progress_info.get_or_create(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                definition_id=payload.chosen_definition_id,
            )
        )

        result = await crud_update_question(self.db, entity, payload)
        cpi_new_score = max(
            0,
            (
                category_progress_info.score + 2
                if result.is_correct
                else category_progress_info.score - 3
            ),
        )
        mpi_new_score = max(
            0,
            (
                meaning_progress_info.score + 2
                if result.is_correct
                else meaning_progress_info.score - 3
            ),
        )
        dpi_new_score = max(
            0,
            (
                definition_progress_info.score + 2
                if result.is_correct
                else definition_progress_info.score - 3
            ),
        )

        if cpi_new_score != category_progress_info.score:
            await self.svc_category_progress_info.update(
                user_id=current_user.id,
                category_id=entity.category_id,
                level_id=entity.level_id,
                payload=CategoryProgressInfoUpdate(
                    score=cpi_new_score,
                ),
            )
        if mpi_new_score != meaning_progress_info.score:
            await self.svc_meaning_progress_info.update(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                level_id=entity.level_id,
                payload=MeaningProgressInfoUpdate(
                    score=mpi_new_score,
                ),
            )
        if dpi_new_score != definition_progress_info.score:
            await self.svc_definition_progress_info.update(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                definition_id=entity.correct_definition_id,
                payload=DefinitionProgressInfoUpdate(
                    score=dpi_new_score,
                ),
            )

        current_progress = await self.svc_statistic.get_level_progress_by_category(
            user_id=current_user.id,
            level_id=entity.level_id,
            category_id=entity.category_id,
        )

        new_cpi = None

        if current_progress >= 100:
            new_cpi = await self.svc_category_progress_info.update_category_level(
                user_id=current_user.id,
                category_id=entity.category_id,
                current_level_id=entity.level_id,
            )

        info = (
            LevelUpInfo(type="level_up", new_level=new_cpi.level.alias)
            if new_cpi
            else None
        )

        return QuestionUpdateOut(
            is_correct=result.is_correct,
            info=info,
        )
