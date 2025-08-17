from app.core.config import settings


def public_url(file_key: str) -> str:
    return f"{settings.R2_PUBLIC_URL.rstrip('/')}/{file_key.lstrip('/')}"
