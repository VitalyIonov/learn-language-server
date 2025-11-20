from fastapi import APIRouter, Query, Depends

from app.core.dependencies.service_factories import get_translation_service
from app.schemas.common import TranslateOut
from app.services.common import TranslationService

router = APIRouter(tags=["translations"])


@router.get("/translate", response_model=TranslateOut, operation_id="getTranslate")
async def translate_text(
    text: str = Query(description="text to translate"),
    svc_translation: TranslationService = Depends(get_translation_service),
):
    result = await svc_translation.translate(text=text)

    return {"translation": result}
