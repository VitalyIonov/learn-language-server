from app.schemas.base import BaseSchema
from app.models.common.question_type import QuestionTypeName


class QuestionTypeOut(BaseSchema):
    id: int
    name: QuestionTypeName

    class Config:
        from_attributes = True


class QuestionTypeListResponse(BaseSchema):
    items: list[QuestionTypeOut]
