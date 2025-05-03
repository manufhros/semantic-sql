import os
from dotenv import load_dotenv

from app.embedding.services.embedding_base import EmbeddingBase
from app.embedding.services.cohere_service import CohereService

load_dotenv()

class EmbeddingFactory:
    @staticmethod
    def create(service_name: str | None = None) -> EmbeddingBase:
        service = service_name or os.getenv("EMBEDDING_PROVIDER", "cohere")
        if service == "cohere":
            return CohereService()
        # elif service == "openai":
        #     return OpenAIService()
        else:
            raise ValueError(f"Unknown embedding service: {service}")