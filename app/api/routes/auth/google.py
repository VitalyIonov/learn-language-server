from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings
from app.core.security import create_access_token
from datetime import timedelta
from fastapi.responses import RedirectResponse
from app.core.dependencies.service_factories import get_user_service
from app.schemas.common import UserCreate
from app.services.common import UserService

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


@router.get("/google/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def auth_callback(request: Request, svc: UserService = Depends(get_user_service)):
    token = await oauth.google.authorize_access_token(request)

    resp = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v3/userinfo", token=token
    )
    user_info = resp.json()

    email = user_info["email"]
    name = user_info.get("name")

    user = await svc.get_by_email(email)
    if not user:
        user = await svc.create(UserCreate(email=email, name=name))

    access_token = create_access_token(
        subject=user.email,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    redirect_url = f"{settings.LOGIN_REDIRECT_URL}"
    redirect = RedirectResponse(url=redirect_url, status_code=303)

    redirect.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        httponly=True,
        samesite="lax",
    )
    return redirect
