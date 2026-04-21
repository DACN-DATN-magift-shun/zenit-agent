from abc import ABC, abstractmethod
from typing import List

from src.data.requests.qdrant_upsert_request import QdrantUpsertRequest


class IQdrant(ABC):
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        pass
    
    @abstractmethod
    def upsert(self, request: QdrantUpsertRequest):
        pass