from typing import List, Dict
from uuid import UUID
from app.vector_store_sdk.vectorstore_client.client import VectorStoreClient
from app.vector_store_sdk.vectorstore_client.models.query import QueryResult

class TableRetriever:
    def __init__(self, vector_client: VectorStoreClient):
        self.client = vector_client

    def retrieve_chunks(self, library_id: UUID, table_extraction: dict) -> List[QueryResult]:
        """
        Given extracted table names and synonyms, query the vector store in a given library.
        Returns matching chunks for each name.
        """
        unique_names = set(table_extraction.get("tables", []))
        unique_names.update(table_extraction.get("aliases_or_synonyms", {}).values())

        all_results = []
        for name in unique_names:
            results = self.client.query(library_id, name, k=3)
            all_results.extend(results)

        return all_results