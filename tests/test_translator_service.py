import pytest
from uuid import UUID
from app.translator.service.translator_service import TranslatorService
from app.translator.types import SQLQuery
from app.vector_store.app.models.query import QueryResult


class MockExtractor:
    def extract(self, query: str) -> dict:
        return {
            "tables": ["customers"],
            "aliases_or_synonyms": {"buyers": "customers"}
        }


class MockVectorClient:
    def query(self, library_id: UUID, query: str):
        return [
            QueryResult(
                chunk_id="8d9e8d12-3c91-4ea5-9ed3-45c5ed0feabc",
                document_id="doc1",
                score=0.95,
                text="Customer table with columns: id, name, email",
                meta={"table_name": "customers", "columns": "id, name, email"}
            )
        ]


class MockGenerator:
    def generate(self, nl_query: str, chunks: list[QueryResult]) -> SQLQuery:
        return SQLQuery(query="SELECT name FROM customers;")


def test_translator_service():
    extractor = MockExtractor()
    vector_client = MockVectorClient()
    generator = MockGenerator()

    service = TranslatorService(extractor, vector_client, generator)

    result = service.translate(
        nl_query="Show all buyers",
        library_id=UUID("b9c91de4-90df-4a33-9a83-c62d3ffef623")
    )

    assert isinstance(result, SQLQuery)
    assert "SELECT" in result.query.upper()
    assert "CUSTOMERS" in result.query.upper()
    print("\nGenerated SQL:", result.query)