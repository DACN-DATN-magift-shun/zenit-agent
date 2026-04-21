from pydantic import BaseModel


class QdrantSearchRequest(BaseModel):
    collection: str
    query: str
    account_id: str