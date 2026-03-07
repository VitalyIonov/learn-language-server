from openai import OpenAI

from app.core.config import settings

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class EmbeddingService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_embeddings(
        self,
        texts: list[str],
        model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> list[list[float]]:
        response = self._client.embeddings.create(
            model=model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def get_embedding(
        self,
        text: str,
        model: str = DEFAULT_EMBEDDING_MODEL,
    ) -> list[float]:
        return self.get_embeddings(texts=[text], model=model)[0]
