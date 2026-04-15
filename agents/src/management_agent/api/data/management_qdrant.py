from fastapi import FastAPI
from qdrant_client import QdrantClient
from src.data.qdrant_base import QdrantBase

class ManagementAgentQdrant(QdrantBase):
    def __init__(self, client: QdrantClient):
        super().__init__(qdrant_client=client)