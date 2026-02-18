from fastapi import APIRouter

from app.constants.target_language import TargetLanguageCode
from app.schemas.common import TargetLanguageOut, TargetLanguageListResponse

router = APIRouter(tags=["target_languages"])


@router.get(
    "/target-languages",
    response_model=TargetLanguageListResponse,
    operation_id="getTargetLanguagesList",
)
async def get_target_languages():
    items = [
        TargetLanguageOut(code=lc, display_name=lc.display_name)
        for lc in TargetLanguageCode
    ]
    return TargetLanguageListResponse(items=items)
