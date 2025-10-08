from fastapi import APIRouter, Query, Depends

from app.core.dependencies.client import get_translate_service
from app.schemas.client import TranslateOut
from app.services.client import TranslateService

router = APIRouter(tags=["translations"])


@router.get("/translate", response_model=TranslateOut)
async def translate_text(
    text: str = Query(description="text to translate"),
    context: str | None = None,
    svc_translate: TranslateService = Depends(get_translate_service),
):
    result = await svc_translate.translate_by_open_ai(text=text, context=context)

    return {"translation": result}
