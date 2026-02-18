from fastapi import APIRouter

from app.constants.interface_language import InterfaceLanguageCode
from app.schemas.common import InterfaceLanguageOut, InterfaceLanguageListResponse

router = APIRouter(tags=["interface_languages"])


@router.get(
    "/interface-languages",
    response_model=InterfaceLanguageListResponse,
    operation_id="getInterfaceLanguagesList",
)
async def get_interface_languages():
    items = [
        InterfaceLanguageOut(code=lc, display_name=lc.display_name)
        for lc in InterfaceLanguageCode
    ]
    return InterfaceLanguageListResponse(items=items)
