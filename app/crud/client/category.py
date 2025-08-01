from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.common import Category
from app.schemas.client import CategoriesListResponse


async def get_categories(
    db: AsyncSession,
) -> CategoriesListResponse:
    statement = select(Category).order_by(Category.name)
    count_statement = select(func.count()).select_from(Category)

    result = await db.execute(statement)
    count = await db.execute(count_statement)

    return CategoriesListResponse.validate(
        {
            "items": result.scalars().all(),
            "meta": {"total_count": count.scalar_one()},
        }
    )
