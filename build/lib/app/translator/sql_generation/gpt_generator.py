from .generator_base import SQLGeneratorBase
from app.vector_store.app.models.query import QueryResult
from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger
import os
import json

load_dotenv()

class GPTSQLGenerator(SQLGeneratorBase):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)
        logger.debug("GPTSQLGenerator initialized with OpenAI API key.")

    def generate(self, query_nl: str, retrieved_chunks: list[QueryResult]) -> str:
        chunks_str = "\n".join(
            f"- Table: {chunk.meta.get('table_name', 'unknown')}\n  Columns: {chunk.meta.get('columns', '')}"
            for chunk in retrieved_chunks
        )

        prompt = f"""
                You are an expert SQL assistant. Your task is to generate an SQL query based on a user's natural language request and the provided schema context.

                Natural Language Query:
                \"\"\"
                {query_nl}
                \"\"\"

                Schema Context:
                {chunks_str}

                Return only the SQL query, nothing else.
                        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful SQL query generator."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()