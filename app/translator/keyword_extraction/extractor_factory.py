import os
from dotenv import load_dotenv

from app.translator.keyword_extraction.extractor_base import ExtractorBase
from app.translator.keyword_extraction.gpt_extractor import GPTExtractor

load_dotenv()  # Carga las variables de entorno desde el .env

class ExtractorFactory:
    @staticmethod
    def create(extractor_name: str | None = None) -> ExtractorBase:
        service = extractor_name or os.getenv("EXTRACTOR_PROVIDER", "gpt")
        if service == "gpt":
            return GPTExtractor()
        # elif service == "openai":
        #     return OpenAIService()
        else:
            raise ValueError(f"Unknown extractor provider: {service}")