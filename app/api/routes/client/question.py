from fastapi import APIRouter, Depends

from app.core.dependencies.common import get_current_user
from app.models import User
from app.schemas.client import QuestionOut
from app.core.dependencies.client import get_question_service
from app.services.client import QuestionService


router = APIRouter(tags=["questions"])


@router.get(
    "/questions/generate",
    response_model=QuestionOut,
)
async def generate_question(
    level_id: int,
    category_id: int,
    svc: QuestionService = Depends(get_question_service),
    current_user: User = Depends(get_current_user),
):
    return await svc.generate(
        category_id=category_id, level_id=level_id, current_user=current_user
    )
