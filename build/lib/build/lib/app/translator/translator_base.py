from abc import ABC, abstractmethod
from .types import QueryInput, SQLQuery

class NL2SQLTranslator(ABC):
    @abstractmethod
    def translate(self, query: QueryInput) -> SQLQuery:
        pass