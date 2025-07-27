from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings
from app.core.db import get_db
from app.crud.user import get_user_by_email, create_user
from app.core.security import create_access_token
from datetime import timedelta
from fastapi.responses import RedirectResponse

oauth = OAuth()
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
    },
)

router = APIRouter(tags=["google-login"])


@router.get("/auth/google/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/google/callback")
async def auth_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    resp = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", token=token
    )
    user_info = resp.json()

    email = user_info["email"]
    name = user_info.get("name")

    user = await get_user_by_email(db, email=email)
    if not user:
        user = await create_user(db, email=email, name=name)

    access_token = create_access_token(
        subject=user.email,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    redirect_url = f"{settings.LOGIN_REDIRECT_URL}?access_token={access_token}"
    return RedirectResponse(url=redirect_url)
