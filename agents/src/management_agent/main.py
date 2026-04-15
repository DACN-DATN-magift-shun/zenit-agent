from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from management_agent.agent import get_agent
from management_agent.api.routes.message_route import management_message_router
from management_agent.common.management_qdrant_constants import ManagementAgentQdrantConstants
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from src.common.env_constants import EnvConstants
from src.common.qdrant_constants import QdrantConstants
import uvicorn

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = await get_agent()
    print("Done initializing agent")
    
    qdrant_client = QdrantClient(url=os.getenv(EnvConstants.QDRANT_CLIENT_URL))
    print("Done initializing Qdrant client")
    
    for collection in ManagementAgentQdrantConstants.QDRANT_COLLECTIONS:
        collections = qdrant_client.get_collections().collections
        existing_names = [c.name for c in collections]
        if collection not in existing_names:
            qdrant_client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(
                    size=QdrantConstants.QDRANT_VECTOR_SIZE,
                    distance=Distance.COSINE
            )
        )
            
        collection_info = qdrant_client.get_collection(collection)
        vector_size = collection_info.config.params.vectors.size
        print(f"Collection '{collection}' created with vector size: {vector_size}")
    yield
    
    qdrant_client.close()
    

app = FastAPI(title="Management Agent API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# Include routes
app.include_router(management_message_router)

if __name__ == "__main__":
    uvicorn.run("management_agent.main:app", host="localhost", port=8765, reload=True, workers=1)



