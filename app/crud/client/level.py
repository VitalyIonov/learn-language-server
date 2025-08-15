from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, case, literal, and_

from app.models import CategoryProgressInfo, Level
from app.schemas.client import LevelsListResponse


async def get_levels(
    db: AsyncSession, user_id: int, category_id: int
) -> LevelsListResponse:
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
        .order_by(Level.alias)
    )

    result = await db.execute(statement)
    orm_items = result.mappings().all()

    return LevelsListResponse.model_validate({"items": orm_items})
