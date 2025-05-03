from abc import ABC, abstractmethod
from typing import List

class ExtractorBase(ABC):
    @abstractmethod
    def extract(self, queryNL: str) -> dict:
        pass