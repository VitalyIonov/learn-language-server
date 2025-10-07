from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, case, literal, and_, exists

from app.models import CategoryProgressInfo, Level, Definition
from app.schemas.client import LevelsListResponse


async def get_levels(
    db: AsyncSession, user_id: int, category_id: int
) -> LevelsListResponse:
    defs_exists = exists().where(
        Definition.level_id == Level.id,
        Definition.category_id == category_id,
    )

    statement = (
        select(
            Level.id,
            Level.name,
            Level.alias,
            Level.value,
            case(
                (CategoryProgressInfo.level_id.is_not(None), literal(False)),
                else_=literal(True),
            ).label("is_locked"),
        )
        .join(
            CategoryProgressInfo,
            and_(
                CategoryProgressInfo.user_id == user_id,
                CategoryProgressInfo.category_id == category_id,
                CategoryProgressInfo.level_id == Level.id,
            ),
            isouter=True,
        )
        .where(defs_exists)
        .order_by(Level.alias)
    )

    result = await db.execute(statement)
    orm_items = result.mappings().all()

    return LevelsListResponse.model_validate({"items": orm_items})
