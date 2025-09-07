from app.schemas.admin import TTSGenerate, TTSGenerateOut
from app.core.config import settings

from openai import OpenAI

DEFAULT_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "marin"


class TTSService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def synthesize(self, params: TTSGenerate) -> TTSGenerateOut:
        resp = self._client.audio.speech.create(
            model=DEFAULT_MODEL,
            voice=DEFAULT_VOICE,
            input=params.text,
        )

        return TTSGenerateOut(content_type="audio/mpeg", data=resp.content)
