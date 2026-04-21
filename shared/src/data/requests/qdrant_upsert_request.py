from typing import Generic, Optional

from pydantic import BaseModel
from src.common.generic_type import T

class QdrantUpsertRequest(BaseModel, Generic[T]):
    collection: str
    query: Optional[str] = None
    payload: T
    