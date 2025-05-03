from fastapi import FastAPI
from app.translator.api import translator

app = FastAPI(title="NL2SQL API")
app.include_router(translator.router)

@app.get("/")
def root():
    return {"message": "Welcome to the NL2SQL API"}