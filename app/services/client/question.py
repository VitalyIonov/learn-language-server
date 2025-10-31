import random
from typing import cast, Union, Type

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from sqlalchemy.orm import load_only

from app.constants.score import BASE_SCORE
from app.schemas.admin import (
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
    LevelOutBase,
    CategoryFinishInfo,
    Info,
)
from app.models import (
    User,
    Meaning,
    Definition,
    Question,
    Level,
    MeaningProgressInfo,
    TextDefinition,
    QuestionTypeName,
    ImageDefinition,
)
from app.crud.client import (
    create_question as crud_create_question,
    get_question as crud_get_question,
    update_question as crud_update_question,
)

from ..admin.category_progress_info import CategoryProgressInfoService
from ..admin.meaning_progress_info import MeaningProgressInfoService
from ..admin.definition_progress_info import DefinitionProgressInfoService
from ..admin.level import LevelService
from .statistic import StatisticService


class QuestionService:
    def __init__(
        self,
        db: AsyncSession,
        svc_category_progress_info: CategoryProgressInfoService,
        svc_meaning_progress_info: MeaningProgressInfoService,
        svc_definition_progress_info: DefinitionProgressInfoService,
        svc_statistic: StatisticService,
        svc_level: LevelService,
    ):
        self.db = db
        self.svc_category_progress_info = svc_category_progress_info
        self.svc_meaning_progress_info = svc_meaning_progress_info
        self.svc_definition_progress_info = svc_definition_progress_info
        self.svc_statistic = svc_statistic
        self.svc_level = svc_level

    def _build_meaning_query(
        self,
        question_level_id: int | None,
        category_id: int,
        user_id: int,
    ):
        current_level_value_stmt = (
            select(Level.value).where(Level.id == question_level_id).scalar_subquery()
        )

        return (
            select(Meaning)
            .join(Level, Meaning.level_id == Level.id)
            .options(load_only(Meaning.id, Meaning.name))
            .join(
                MeaningProgressInfo,
                and_(
                    MeaningProgressInfo.meaning_id == Meaning.id,
                    MeaningProgressInfo.level_id == question_level_id,
                    MeaningProgressInfo.user_id == user_id,
                ),
                isouter=True,
            )
            .where(
                Meaning.definitions.any(Definition.level_id == question_level_id),
                Meaning.category_id == category_id,
                Level.value <= current_level_value_stmt,
            )
            .order_by(
                case(
                    (func.coalesce(MeaningProgressInfo.score, 0) < BASE_SCORE, 1),
                    else_=2,
                ),
                func.random(),
            )
            .limit(1)
        )

    async def generate(
        self, payload: QuestionGenerate, current_user: User
    ) -> QuestionOut:
        question_level = await self.svc_level.get(payload.level_id)

        meaning_stmt = self._build_meaning_query(
            question_level_id=question_level.id,
            category_id=payload.category_id,
            user_id=current_user.id,
        )
        meaning = (await self.db.execute(meaning_stmt)).scalars().one_or_none()

        if meaning is None:
            raise NoResultFound("Meaning not found")

        question_type = question_level.question_types[0]
        definition_class: Union[Type[TextDefinition], Type[ImageDefinition]]

        if question_type.name == QuestionTypeName.TEXT:
            definition_class = TextDefinition
            load_fields = [definition_class.id, definition_class.text]
            false_definitions_count = 2
        else:
            definition_class = ImageDefinition
            load_fields = [definition_class.id, definition_class.image_id]
            false_definitions_count = 3

        definition_false_stmt = (
            select(definition_class)
            .options(load_only(*load_fields))
            .where(
                definition_class.level_id == question_level.id,
                definition_class.category_id == payload.category_id,
                ~definition_class.meanings.any(Meaning.id == meaning.id),
            )
            .order_by(func.random())
            .limit(false_definitions_count)
        )

        definition_true_stmt = (
            select(definition_class)
            .options(load_only(*load_fields))
            .where(
                definition_class.level_id == question_level.id,
                definition_class.meanings.any(Meaning.id == meaning.id),
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
            type=question_type.name,
            meaning_id=cast(int, meaning.id),
            category_id=payload.category_id,
            level_id=question_level.id,
            correct_definition_id=cast(int, true_definition.id),
        )

        question = await crud_create_question(self.db, question_data, definition_ids)

        return QuestionOut.model_validate(
            {
                "id": question.id,
                "type": question.type,
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

        update_result = None
        update_info: Info | None = None

        if current_progress >= 100:
            update_result = await self.svc_category_progress_info.update_category_level(
                user_id=current_user.id,
                category_id=entity.category_id,
                current_level_id=entity.level_id,
            )

        if update_result is not None:
            if update_result.new_next_cpi is not None:
                update_info = LevelUpInfo(
                    type="level_up",
                    new_level=LevelOutBase.model_validate(
                        update_result.new_next_cpi.level
                    ),
                )
            elif update_result.next_level is None:
                update_info = CategoryFinishInfo(
                    type="category_finish",
                )

        return QuestionUpdateOut(
            is_correct=result.is_correct,
            info=update_info,
        )
