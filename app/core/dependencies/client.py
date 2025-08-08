from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.client import CategoryService, QuestionService


async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(db)


async def get_question_service(db: AsyncSession = Depends(get_db)) -> QuestionService:
    return QuestionService(db)
