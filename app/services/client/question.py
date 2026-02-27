import random

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.score import DEFINITION_GROUP_SCORES
from app.constants.definition import DefinitionGroup, FALSE_DEFINITIONS_COUNT
from app.schemas.admin import (
    MeaningProgressInfoUpdate,
    DefinitionProgressInfoUpdate,
)

from app.schemas.client import (
    DefinitionCandidate,
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
    Question,
)
from app.crud.client import (
    create_question as crud_create_question,
    get_question as crud_get_question,
    update_question as crud_update_question,
    get_definition_candidates as crud_get_definition_candidates,
    get_definitions_by_ids as crud_get_definitions_by_ids,
    get_meaning as crud_get_meaning,
)

from ..admin.category_progress_info import CategoryProgressInfoService
from ..admin.meaning_progress_info import MeaningProgressInfoService
from ..admin.definition_progress_info import DefinitionProgressInfoService
from .statistic import StatisticService


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

    @staticmethod
    def _compute_false_definition_ids(
        candidates: list[DefinitionCandidate],
    ) -> dict[tuple[int, int], set[int]]:
        group_definitions: dict[DefinitionGroup, set[int]] = {}
        meaning_definitions: dict[int, set[int]] = {}

        for candidate in candidates:
            group_definitions.setdefault(candidate.group, set()).add(candidate.definition_id)
            meaning_definitions.setdefault(candidate.meaning_id, set()).add(candidate.definition_id)

        return {
            (candidate.definition_id, candidate.meaning_id): group_definitions[candidate.group] - meaning_definitions[candidate.meaning_id]
            for candidate in candidates
        }

    async def generate(self, payload: QuestionGenerate, current_user: User) -> QuestionOut:
        definition_candidates = await crud_get_definition_candidates(
            self.db,
            level_id=payload.level_id,
            category_id=payload.category_id,
            user_id=current_user.id,
        )

        if not definition_candidates:
            raise NoResultFound("No definitions found")

        false_ids_map = self._compute_false_definition_ids(definition_candidates)

        eligible = [
            candidate
            for candidate in definition_candidates
            if len(false_ids_map[(candidate.definition_id, candidate.meaning_id)]) >= FALSE_DEFINITIONS_COUNT[candidate.group]
        ]

        if not eligible:
            raise NoResultFound("No eligible definitions found")

        selected = random.choices(eligible, weights=[candidate.chance for candidate in eligible], k=1)[0]

        n = FALSE_DEFINITIONS_COUNT[selected.group]
        false_definition_ids = random.sample(list(false_ids_map[(selected.definition_id, selected.meaning_id)]), n)

        all_definition_ids = [selected.definition_id] + false_definition_ids
        definitions = await crud_get_definitions_by_ids(self.db, definition_ids=all_definition_ids, definition_type=selected.type)

        meaning = await crud_get_meaning(self.db, meaning_id=selected.meaning_id)
        if meaning is None:
            raise NoResultFound("Meaning not found")

        random.shuffle(definitions)
        definition_ids = [definition.id for definition in definitions]

        question_data = QuestionCreate(
            user_id=current_user.id,
            type=selected.type,
            meaning_id=selected.meaning_id,
            category_id=payload.category_id,
            level_id=payload.level_id,
            correct_definition_id=selected.definition_id,
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
            category_id=entity.category_id,
        )
        definition_progress_info = await self.svc_definition_progress_info.get_or_create(
            user_id=current_user.id,
            meaning_id=entity.meaning_id,
            definition_id=payload.chosen_definition_id,
            level_id=entity.level_id,
            category_id=entity.category_id,
        )

        result = await crud_update_question(self.db, entity, payload)

        if result.is_correct and entity.correct_definition:
            group_score = DEFINITION_GROUP_SCORES.get(entity.correct_definition.group, 0)
            mpi_new_score = meaning_progress_info.score + group_score
            new_chance = round(definition_progress_info.chance * 0.8, 2)
        else:
            mpi_new_score = meaning_progress_info.score
            new_chance = round(definition_progress_info.chance * 1.3, 2)

        if mpi_new_score != meaning_progress_info.score:
            await self.svc_meaning_progress_info.update(
                user_id=current_user.id,
                meaning_id=entity.meaning_id,
                level_id=entity.level_id,
                payload=MeaningProgressInfoUpdate(
                    score=mpi_new_score,
                ),
            )

        await self.svc_definition_progress_info.update(
            user_id=current_user.id,
            meaning_id=entity.meaning_id,
            definition_id=payload.chosen_definition_id,
            payload=DefinitionProgressInfoUpdate(chance=new_chance),
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
                level_id=entity.level_id,
            )

        if update_result is not None:
            if update_result.new_next_cpi is not None:
                update_info = LevelUpInfo(
                    type="level_up",
                    new_level=LevelOutBase.model_validate(update_result.new_next_cpi.level),
                )
            elif update_result.next_level is None:
                update_info = CategoryFinishInfo(
                    type="category_finish",
                )

        return QuestionUpdateOut(
            is_correct=result.is_correct,
            info=update_info,
        )
