from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.target_language import TargetLanguageCode
from app.crud.client import (
    get_category as crud_get_category,
    get_categories as crud_get_categories,
)
from app.crud.common import (
    get_all_definition_stats as crud_get_all_definition_stats,
    get_scores_by_categories as crud_get_scores_by_categories,
)
from app.schemas.client import CategoriesListResponse, CategoryOut, CategoryOutBase
from app.schemas.common import Meta
from app.services.client.statistic import _get_category_max_scores
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

    async def get_all(self, user_id: int, target_language: TargetLanguageCode) -> CategoriesListResponse:
        categories, total_count = await crud_get_categories(self.db)

        stat_rows = await crud_get_all_definition_stats(self.db, language=target_language)
        max_scores = _get_category_max_scores(stat_rows)

        category_ids = [category.id for category in categories]
        current_scores = await crud_get_scores_by_categories(
            self.db, user_id=user_id, category_ids=category_ids, language=target_language
        )

        items = []
        for category in categories:
            translated_name = await self.svc_translation.translate(
                text=category.name,
                lang_from=category.language,
                lang_to=target_language,
            )
            items.append(
                CategoryOutBase(
                    id=category.id,
                    name=translated_name,
                    language=category.language,
                    image=category.image,
                    current_score=current_scores.get(category.id, 0),
                    max_score=max_scores.get(category.id, 0),
                )
            )

        return CategoriesListResponse(items=items, meta=Meta(total_count=total_count))
