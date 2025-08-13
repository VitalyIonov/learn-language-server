from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_level_service
from app.core.dependencies.common import get_current_user
from app.models import User
from app.schemas.client import (
    QuestionOut,
    QuestionGenerate,
    QuestionUpdate,
    QuestionUpdateOut,
)
from app.core.dependencies.client import get_question_service
from app.services.admin import LevelService
from app.services.client import QuestionService


router = APIRouter(tags=["questions"])


@router.post(
    "/questions/generate",
    response_model=QuestionOut,
)
async def generate_question(
    payload: QuestionGenerate,
    svc: QuestionService = Depends(get_question_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.generate(payload, current_user=current_user)


@router.patch("/questions/{question_id}", response_model=QuestionUpdateOut)
async def update_question_endpoint(
    question_id: int,
    payload: QuestionUpdate,
    svc_question: QuestionService = Depends(get_question_service),
    svc_level: LevelService = Depends(get_level_service),
    current_user: User = Depends(get_current_user),
):
    return await svc_question.update(svc_level, question_id, payload, current_user)
