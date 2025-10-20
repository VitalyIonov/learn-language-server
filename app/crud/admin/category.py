from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from app.models.common import Category
from app.schemas.admin import CategoryCreate, CategoriesListResponse, CategoryUpdate
from typing import Optional


async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    return await db.get(Category, category_id)


async def create_category(db: AsyncSession, new_category: CategoryCreate) -> Category:
    category = Category(**new_category.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(
    db: AsyncSession, db_category: Category, payload: CategoryUpdate
) -> Category:
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_category, field, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    stmt = delete(Category).where(Category.id == category_id).returning(Category.id)
    result = await db.execute(stmt)
    await db.commit()
    deleted_id = result.scalar_one_or_none()
    return deleted_id is not None


async def get_categories(
    db: AsyncSession,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    q: Optional[str] = None,
) -> CategoriesListResponse:
    statement = select(Category).order_by(Category.name)
    count_statement = select(func.count()).select_from(Category)

    if q:
        statement = statement.where(Category.name.ilike(f"%{q}%"))
        count_statement = count_statement.where(Category.name.ilike(f"%{q}%"))

    if offset is not None and limit is not None:
        statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    count = await db.execute(count_statement)

    return CategoriesListResponse.model_validate(
        {
            "items": result.scalars().all(),
            "meta": {"total_count": count.scalar_one()},
        }
    )
