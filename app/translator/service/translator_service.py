from uuid import UUID
from typing import Any

from app.translator.types import SQLQuery
from app.translator.keyword_extraction.extractor_base import ExtractorBase
from app.vector_store_sdk.vectorstore_client.client import VectorStoreClient
from app.translator.sql_generation.generator_base import SQLGeneratorBase


class TranslatorService:
    """
    Main service that coordinates natural language to SQL translation.
    It uses:
    - an extractor to detect relevant tables and synonyms from NL query
    - a vector store to retrieve relevant chunks
    - a SQL generator to produce the final SQL query
    """

    def __init__(
        self,
        extractor: ExtractorBase,
        vector_client: VectorStoreClient,
        generator: SQLGeneratorBase,
    ):
        self.extractor = extractor
        self.vector_client = vector_client
        self.generator = generator

    def translate_to_sql(self, nl_query: str, library_id: UUID) -> SQLQuery:
        """
        Given a natural language query and a vector library, returns an SQLQuery.
        """
        extraction: dict[str, Any] = self.extractor.extract(nl_query)
        if not isinstance(extraction, dict):
            raise ValueError("Extractor must return a dict with 'aliases_or_synonyms'")

        # Enrich the query with aliases/synonyms if available
        enriched_query = nl_query
        for alias, real_table in extraction.get("aliases_or_synonyms", {}).items():
            if alias.lower() not in enriched_query.lower():
                enriched_query += f" {alias}"

        # Perform vector search to get relevant chunks
        retrieved_chunks = self.vector_client.query(
            library_id=library_id, query=enriched_query
        )

        # Generate SQL query using original NL query and retrieved context
        sql_string = self.generator.generate(nl_query, retrieved_chunks)
        return SQLQuery(query=sql_string)