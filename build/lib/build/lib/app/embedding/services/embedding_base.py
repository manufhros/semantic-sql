from abc import ABC, abstractmethod
from typing import List

class EmbeddingBase(ABC):
    @abstractmethod
    def get_embedding(self, query: str, input_type: str = "search_query") -> List[float]:
        pass