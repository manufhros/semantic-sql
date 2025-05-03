from uuid import UUID
from .types import SQLQuery

class TranslatorService:
    def __init__(self, extractor, vector_client, generator):
        self.extractor = extractor
        self.vector_client = vector_client
        self.generator = generator

    def translate(self, nl_query: str, library_id: UUID) -> SQLQuery:
        extraction = self.extractor.extract(nl_query)

        # Expande la query con sinónimos extraídos
        enriched_query = nl_query
        aliases = extraction.get("aliases_or_synonyms", {})
        if isinstance(aliases, dict):
            for alias, real_table in aliases.items():
                if alias not in enriched_query:
                    enriched_query += f" {alias}"

        # Consulta chunks en la base vectorial usando la query enriquecida
        retrieved_chunks = self.vector_client.query(library_id, query=enriched_query)

        # Genera la SQL final basada en la consulta original + chunks
        return self.generator.generate(nl_query, retrieved_chunks)