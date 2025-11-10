from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get("access_token")
        if token:
            return token

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return None
