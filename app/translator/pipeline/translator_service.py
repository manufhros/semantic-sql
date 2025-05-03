from uuid import UUID
from .types import SQLQuery
from app.translator.keyword_extraction.extractor_base import ExtractorBase
from app.vector_store_sdk.vectorstore_client.client import VectorStoreClient
from app.translator.sql_generation.generator_base import SQLGeneratorBase

class TranslatorService:
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
        extraction = self.extractor.extract(nl_query)
        if not isinstance(extraction, dict):
            raise ValueError("Extractor must return a dict with 'aliases_or_synonyms'")

        # Expande la query con sinónimos extraídos
        enriched_query = nl_query
        aliases = extraction.get("aliases_or_synonyms", {})
        for alias in aliases:
            if alias.lower() not in enriched_query.lower():
                enriched_query += f" {alias}"

        # Consulta chunks en la base vectorial usando la query enriquecida
        retrieved_chunks = self.vector_client.query(library_id, query=enriched_query)
        # Genera la SQL final basada en la consulta original + chunks
        return self.generator.generate(nl_query, retrieved_chunks)