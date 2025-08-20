from app.schemas.common import BaseSchema


class QuestionTypeOut(BaseSchema):
    id: int
    name: str

    class Config:
        from_attributes = True


class QuestionTypeListResponse(BaseSchema):
    items: list[QuestionTypeOut]
