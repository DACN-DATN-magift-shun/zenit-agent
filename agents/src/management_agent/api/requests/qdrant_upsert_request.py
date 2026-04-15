from pydantic import BaseModel
from src.data.requests.qdrant_upsert_request import QdrantUpsertRequest

class TransactionPayload(BaseModel):
    title: str
    category: str
    wallet: str
    account_id: str

class ManagementAgentQdrantUpsertRequest(QdrantUpsertRequest[TransactionPayload]):
    payload: TransactionPayload