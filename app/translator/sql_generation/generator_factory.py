import os
from dotenv import load_dotenv
from .generator_base import SQLGeneratorBase
from .gpt_generator import GPTSQLGenerator

load_dotenv()

class SQLGeneratorFactory:
    @staticmethod
    def create(generator_name: str | None = None) -> SQLGeneratorBase:
        name = generator_name or os.getenv("GENERATOR_PROVIDER", "gpt")
        if name == "gpt":
            return GPTSQLGenerator()
        raise ValueError(f"Unknown generator provider: {name}")