import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.translator.api import translator_routes
from app.translator.service.translator_service import TranslatorService
from app.translator.keyword_extraction.gpt_extractor import GPTExtractor
from app.translator.sql_generation.gpt_generator import GPTSQLGenerator
from app.vector_store_sdk.vectorstore_client.client import VectorStoreClient
from app.translator.api.translator_routes import get_router


load_dotenv()

app = FastAPI(title="NL2SQL API")

extractor = GPTExtractor()  # <- no CohereService aquí
generator = GPTSQLGenerator()

base_url = os.getenv("VECTOR_STORE_URL", "http://localhost:8000")
vector_client = VectorStoreClient(base_url=base_url)

translator_service = TranslatorService(
    extractor=extractor,
    vector_client=vector_client,
    generator=generator,
)

# Pasa translator_service al router (debes tener algo como esto)

app.include_router(get_router(translator_service))

@app.get("/")
def root():
    return {"message": "Welcome to the NL2SQL API"}