from abc import ABC, abstractmethod
from typing import List
from app.vector_store_sdk.vectorstore_client.models.query import QueryResult

class SQLGeneratorBase(ABC):
    @abstractmethod
    def generate(self, query_nl: str, retrieved_chunks: List[QueryResult]) -> str:
        """Generate SQL query from natural language and retrieved chunk context"""
        pass