from sqlalchemy.ext.asyncio import AsyncSession
from app.models.common import User
from app.schemas.client import SettingsUpdate


async def update_settings(
    db: AsyncSession, db_user: User, settings_update: SettingsUpdate
) -> User:
    update_data = settings_update.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(db_user, field, value)

    await db.commit()
    await db.refresh(db_user)

    return db_user
