from .extractor_base import ExtractorBase
from typing import List
from openai import OpenAI
import os
from loguru import logger
from dotenv import load_dotenv
import json

load_dotenv()

class GPTExtractor(ExtractorBase):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found in environment variables.")
        self.client = OpenAI(api_key=api_key)
        logger.debug("GPTExtractor initialized with OpenAI API key.")

    def extract(self, queryNL: str) -> dict:
        prompt = f"""
                You are an expert assistant in SQL databases. Your task is to analyze a query written in natural language and return a JSON object with the following information:

                1. "tables": A list of table names that are mentioned or implied in the query.
                2. "aliases_or_synonyms": A dictionary where the keys are aliases, synonyms, or common informal terms found in the query (including verbs or indirect references), and the values are the corresponding actual table names if they can be inferred.

                Be sure to extract not only explicitly named tables but also implied ones, and identify any synonyms or alternate terms that refer to those tables.

                Do not include any explanations. Return only the JSON.

                Query:
                ---
                {queryNL}
                """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert assistant in semantic analysis of SQL databases."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            content = response.choices[0].message.content

            parsed = json.loads(content)
            parsed["aliases_or_synonyms"] = {
                k: v for k, v in parsed.get("aliases_or_synonyms", {}).items() if k.lower() != v.lower()
            }
            return parsed

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON returned by OpenAI: {}", content)
            raise ValueError("GPT response is not valid JSON") from e