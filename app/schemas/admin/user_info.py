from app.schemas.common import BaseSchema


class UserInfoOut(BaseSchema):
    id: int
    user_id: int
    current_question_id: int

    class Config:
        from_attributes = True


class UserInfoCreate(BaseSchema):
    user_id: int


class UserInfoUpdate(BaseSchema):
    current_question_id: int
