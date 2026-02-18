from fastapi import APIRouter, Depends, Response, Request

from app.core.dependencies.service_factories import (
    get_current_user,
    get_settings_service,
)
from app.models import User
from app.schemas.client import SettingsInterfaceLangUpdate, SettingsTargetLanguageUpdate
from app.services.client import SettingsService
from app.utils.cookies import build_interface_lang_cookie

router = APIRouter(tags=["settings"])


@router.patch("/settings/interface-lang", response_model=bool, operation_id="updateSettingsInterfaceLanguage")
async def update_interface_language(
    payload: SettingsInterfaceLangUpdate,
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user),
    svc: SettingsService = Depends(get_settings_service),
):
    await svc.update_interface_language(current_user, payload)

    cookie = build_interface_lang_cookie(payload.interface_lang.value, request=request)
    response.set_cookie(**cookie)

    return True


@router.patch("/settings/target-language", response_model=bool, operation_id="updateSettingsTargetLanguage")
async def update_target_language(
    payload: SettingsTargetLanguageUpdate,
    current_user: User = Depends(get_current_user),
    svc: SettingsService = Depends(get_settings_service),
):
    return await svc.update_target_language(current_user, payload)
