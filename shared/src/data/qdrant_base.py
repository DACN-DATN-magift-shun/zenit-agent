from typing import List
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, MatchValue, Filter, PointStruct
from src.common.qdrant_constants import QdrantConstants
from src.data.interfaces.i_qdrant import IQdrant
from src.data.requests.qdrant_search_request import QdrantSearchRequest
from src.data.requests.qdrant_upsert_request import QdrantUpsertRequest
from src.utils.llm_util import LLMUtil


class QdrantBase(IQdrant):
    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.embedding_model = LLMUtil.get_google_genai_embedding_model()
        
    
    def embed(self, text: str) -> List[float]:
        embedding = self.embedding_model.embed_query(text)
        return embedding
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.embedding_model.embed_documents(texts)
        return embeddings
    
    def upsert(self, request: QdrantUpsertRequest):
        if issubclass(type(request), QdrantUpsertRequest) and type(request) is not QdrantUpsertRequest:
            self.qdrant_client.upsert(
                collection_name=request.collection,
                points=[
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=self.embed(request.query),
                        payload=request.payload.model_dump()
                    )
                ]
            )
    
    def search(self, request: QdrantSearchRequest):
        embedding = self.embed(request.query)
        search_result = self.qdrant_client.query_points(
            collection_name=request.collection,
            query=embedding,
            limit=QdrantConstants.QDRANT_SEARCH_K,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="account_id",
                        match=MatchValue(value=request.account_id)
                    )
                ]
            )
        )
        
        return search_result