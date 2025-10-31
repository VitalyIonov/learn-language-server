from fastapi import APIRouter, Depends

from app.core.dependencies.service_factories import get_current_user
from app.models import User
from app.schemas.client import (
    QuestionOut,
    QuestionGenerate,
    QuestionUpdate,
    QuestionUpdateOut,
)
from app.core.dependencies.service_factories import get_question_service
from app.services.client import QuestionService


router = APIRouter(tags=["questions"])


@router.post(
    "/questions/generate",
    response_model=QuestionOut,
)
async def generate_question(
    payload: QuestionGenerate,
    svc_question: QuestionService = Depends(get_question_service),
    current_user: User = Depends(get_current_user),
):
    return await svc_question.generate(payload, current_user=current_user)


@router.patch("/questions/{question_id}", response_model=QuestionUpdateOut)
async def update_question_endpoint(
    question_id: int,
    payload: QuestionUpdate,
    svc_question: QuestionService = Depends(get_question_service),
    current_user: User = Depends(get_current_user),
):
    return await svc_question.update(question_id, payload, current_user)
