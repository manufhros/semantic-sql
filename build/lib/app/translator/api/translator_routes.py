from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.translator.service.translator_service import TranslatorService
from app.embedding.services.embedding_factory import EmbeddingFactory
from app.translator.sql_generation.gpt_generator import GPTSQLGenerator
from app.vector_store_sdk.vectorstore_client.client import VectorStoreClient

from app.translator.types import SQLQuery

router = APIRouter(prefix="/libraries/{library_id}/translate", tags=["translation"])


class TranslationRequest(BaseModel):
    query: str


@router.post("/", response_model=SQLQuery)
def translate_query(library_id: UUID, request: TranslationRequest):
    try:
        service = TranslatorService(
            extractor=EmbeddingFactory.create(),
            vector_client=VectorStoreClient(base_url="http://localhost:8001"),  # Ajusta la URL
            generator=GPTSQLGenerator()
        )

        return service.translate(request.query, library_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))