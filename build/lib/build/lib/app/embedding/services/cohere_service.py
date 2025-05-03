from .embedding_base import EmbeddingBase
from typing import List
import os
import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

class CohereService(EmbeddingBase):
    def __init__(self):
        if not COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY not set in environment variables")
        self.client = cohere.Client(COHERE_API_KEY)

    def get_embedding(self, query: str, input_type: str = "search_query") -> List[float]:
        try:
            response = self.client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type=input_type,
            )
            return response.embeddings[0]
        except Exception as e:
            raise RuntimeError(f"Error generating embedding: {str(e)}") from e