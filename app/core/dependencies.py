from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.db import get_db
from app.services.auth import AuthService
from app.services.user import UserService
from app.services.meaning import MeaningService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_meaning_service(db: AsyncSession = Depends(get_db)) -> MeaningService:
    return MeaningService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_svc: UserService = Depends(get_user_service),
) -> User:
    email = AuthService.decode_token(token)
    return await user_svc.get_by_email(email)


async def require_admin(
    current_user: User = Depends(get_current_user),
    user_svc: UserService = Depends(get_user_service),
) -> User:
    await user_svc.require_admin(current_user)
    return current_user
