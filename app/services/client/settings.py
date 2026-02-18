from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.client import (
    update_settings as crud_update_settings,
)
from app.models import User
from app.schemas.client import SettingsInterfaceLangUpdate


class SettingsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_language(self, user: User, payload: SettingsInterfaceLangUpdate) -> bool:
        updated_user = await crud_update_settings(self.db, user, payload)

        return True if updated_user else False
