from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.category import Category
from app.schemas import CategoryCreate, CategoriesListResponse
from typing import Optional
from app.constants.data import DEFAULT_OFFSET, DEFAULT_LIMIT


async def create_category(db: AsyncSession, new_category: CategoryCreate) -> Category:
    category = Category(**new_category.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories(
    db: AsyncSession,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    q: Optional[str] = None,
) -> CategoriesListResponse:
    statement = select(Category).order_by(Category.name)
    count_statement = select(func.count()).select_from(Category)

    if q:
        statement = statement.where(Category.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(Category.name.ilike(f"%{q}%"))

    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    count = await db.execute(count_statement)

    return CategoriesListResponse.validate(
        {
            "items": result.scalars().all(),
            "meta": {"total_count": count.scalar_one()},
        }
    )
