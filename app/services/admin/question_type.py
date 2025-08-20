from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.admin import get_question_types as crud_get_question_types


class QuestionTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        return await crud_get_question_types(self.db)
