from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.target_language import TargetLanguageCode
from app.crud.client import (
    get_category as crud_get_category,
    get_categories as crud_get_categories,
)
from app.schemas.client import CategoriesListResponse, CategoryOut
from app.services.common import TranslationService


class CategoryService:
    def __init__(self, db: AsyncSession, svc_translation: TranslationService):
        self.db = db
        self.svc_translation = svc_translation

    async def get(self, category_id: int, target_language: TargetLanguageCode) -> CategoryOut:
        category = await crud_get_category(self.db, category_id=category_id)

        if category is None:
            raise NoResultFound("Category not found")

        result = CategoryOut.model_validate(category)
        result.name = await self.svc_translation.translate(
            text=result.name,
            lang_from=category.language,
            lang_to=target_language,
        )

        return result

    async def get_all(self, target_language: TargetLanguageCode) -> CategoriesListResponse:
        response = await crud_get_categories(self.db)

        for item in response.items:
            item.name = await self.svc_translation.translate(
                text=item.name,
                lang_from=item.language,
                lang_to=target_language,
            )

        return response
