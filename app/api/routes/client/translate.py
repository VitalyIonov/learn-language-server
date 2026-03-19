from fastapi import APIRouter, Query, Depends

from app.constants.target_language import TargetLanguageCode
from app.core.dependencies.service_factories import get_translation_service
from app.schemas.common import TranslateOut
from app.services.common import TranslationService

router = APIRouter(tags=["translations"])


@router.get("/translate", response_model=TranslateOut, operation_id="getTranslate")
async def translate_text(
    text: str = Query(description="text to translate"),
    lang_from: TargetLanguageCode = Query(description="source language code"),
    lang_to: TargetLanguageCode = Query(description="target language code"),
    context: str | None = Query(default=None, description="optional context for better translation"),
    svc_translation: TranslationService = Depends(get_translation_service),
):
    result = await svc_translation.translate(text=text, lang_from=lang_from, lang_to=lang_to, context=context)

    return {"translation": result}
