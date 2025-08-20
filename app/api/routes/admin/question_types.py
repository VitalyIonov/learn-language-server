from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_question_type_service
from app.schemas.admin import QuestionTypeListResponse
from app.services.admin import QuestionTypeService

router = APIRouter(tags=["question_types"])


@router.get("/question_types", response_model=QuestionTypeListResponse)
async def read_question_types(
    svc_question_type: QuestionTypeService = Depends(get_question_type_service),
):
    return await svc_question_type.get_all()
