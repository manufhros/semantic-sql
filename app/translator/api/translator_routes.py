from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.translator.service.translator_service import TranslatorService
from app.translator.types import SQLQuery


class TranslationRequest(BaseModel):
    query: str


def get_router(translator_service: TranslatorService) -> APIRouter:
    router = APIRouter(prefix="/libraries/{library_id}/translate", tags=["translator"])

    @router.post("/", response_model=SQLQuery)
    def translate_query(library_id: UUID, request: TranslationRequest):
        try:
            return translator_service.translate_to_sql(request.query, library_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router