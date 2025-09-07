from fastapi import APIRouter, Depends

from app.core.dependencies.admin import get_tts_service
from app.schemas.admin import TTSGenerate, TTSGenerateOut
from app.services.admin import TTSService

router = APIRouter(tags=["test_tts"])


@router.post("/test_tts", response_model=TTSGenerateOut)
async def synthesize_audio(
    body: TTSGenerate,
    svc_tts: TTSService = Depends(get_tts_service),
):
    return await svc_tts.synthesize(body)
