# Management Agent

This agent is a FastAPI application that uses LangGraph to create a conversational agent.

## Prerequisites

- Python 3.12+
- Docker Desktop

## Setup

### 1. Environment Variables

Create a `.env` file in the `agents/src/management_agent` directory with the following content:

```env
# Google AI
GOOGLE_AI_API_KEY=your_google_ai_api_key
GOOGLE_CHAT_MODEL_NAME=gemini-1.5-pro-latest
GOOGLE_EMBEDDING_MODEL_NAME=text-embedding-004

# Qdrant
QDRANT_CLIENT_URL=http://localhost:6333

# Management API
MANAGEMENT_API_BASE_URL=http://localhost:8000
MANAGEMENT_POSTGRES_URL=postgresql+psycopg://user:password@localhost:5432/dbname

# Authentication
TEST_ACCESS_TOKEN=your_test_access_token
AUTH_USERNAME=your_auth_username
AUTH_PASSWORD=your_auth_password
```

Replace the placeholder values with your actual credentials.

### 2. Start Infrastructure

The agent requires a Qdrant vector database. You can start it using the provided Docker Compose file.

```bash
docker-compose -f infrastructures/docker-compose.yml up -d
```

## 3. Running the Agent

Once the setup is complete, you can run the agent using `uvicorn`.

```bash
cd agents
uv run uvicorn management_agent.main:app --host localhost --port 8765 --reload
```

The API will be available at `http://localhost:8765`. You can access the OpenAPI documentation at `http://localhost:8765/docs`.
