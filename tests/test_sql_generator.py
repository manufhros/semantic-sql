import os
import pytest
from uuid import uuid4
from app.translator.sql_generation.gpt_generator import GPTSQLGenerator
from app.vector_store.app.models.query import QueryResult, QueryRequest

@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set in environment"
)
def test_generate_sql_query():
    generator = GPTSQLGenerator()

    query = "Show me all customers who bought products last month"

    retrieved_chunks = [
        QueryResult(
            chunk_id=uuid4(),
            document_id=uuid4(),
            score=0.95,
            text="Customer table with columns: id, name, email, signup_date",
            meta={"table_name": "customers", "columns": "id, name, email, signup_date"}
        ),
        QueryResult(
            chunk_id=uuid4(),
            document_id=uuid4(),
            score=0.93,
            text="Orders table with columns: id, customer_id, product_id, order_date",
            meta={"table_name": "orders", "columns": "id, customer_id, product_id, order_date"}
        ),
    ]

    sql = generator.generate(query, retrieved_chunks)

    assert "SELECT" in sql.upper()
    assert "FROM" in sql.upper()
    print("\nGenerated SQL:\n", sql)