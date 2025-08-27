from fastapi import APIRouter, Query
from app.schemas.client import TranslateOut
from app.services.client import DeepLTranslateService

router = APIRouter(tags=["translations"])


@router.get("/translate", response_model=TranslateOut)
async def translate_text(
    text: str = Query(description="text to translate"),
):
    result = DeepLTranslateService.translate(text)

    return {"translation": result}
