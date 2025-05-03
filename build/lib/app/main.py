from fastapi import FastAPI
from dotenv import load_dotenv
from app.translator.api import translator_routes

load_dotenv()

app = FastAPI(
    title="Semantic SQL Translator API",
    description="Translate natural language queries into SQL using vector search and LLMs.",
    version="0.1.0",
)

# Rutas del traductor
app.include_router(translator_routes.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Semantic SQL Translator API"}