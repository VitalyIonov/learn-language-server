from jose import JWTError, jwt
from app.core.config import settings
from fastapi import HTTPException, status


class AuthService:
    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            sub = payload.get("sub")
            if sub is None:
                raise JWTError()
            return sub
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
