from fastapi import APIRouter, Depends, Response, Request

from app.core.dependencies.service_factories import (
    get_current_user,
    get_settings_service,
)
from app.models import User
from app.schemas.client import SettingsLangUpdate
from app.services.client import SettingsService

router = APIRouter(tags=["settings"])


def build_lang_cookie(lang: str, *, request: Request) -> dict:
    cookie = {
        "key": "lang",
        "value": lang,
        "max_age": 60 * 60 * 24 * 365,
        "path": "/",
        "httponly": True,
        "samesite": "lax",
        "secure": request.url.scheme == "https",
    }
    host = request.url.hostname or ""
    if host.endswith("learn-language.es"):
        cookie["domain"] = ".learn-language.es"
    return cookie


@router.patch("/settings/lang", response_model=bool)
async def update_language(
    payload: SettingsLangUpdate,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    svc: SettingsService = Depends(get_settings_service),
):
    lang = payload.lang
    await svc.update_language(current_user, payload)

    cookie = build_lang_cookie(lang, request=request)
    response.set_cookie(**cookie)

    return True
