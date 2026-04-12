# Build stage
FROM python:3.12-slim AS builder

WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

# Restore dependencies as distinct layers
COPY ["./pyproject.toml", "./"]
COPY ["shared/pyproject.toml", "shared/"]
COPY ["agents/pyproject.toml", "agents/"]
COPY ["agents/README.md", "agents/"]        
COPY ["shared/README.md", "shared/"] 

COPY ["shared/src/", "shared/src/"]
COPY ["agents/src/", "agents/src/"]
COPY ["agents/langgraph.json", "agents/"]
RUN uv sync --all-packages --no-dev

# Copy source code
COPY ["./.gitignore", "./"]
COPY ["agents/.gitignore", "agents/"]
COPY ["agents/AGENTS.md", "agents/"]
COPY ["shared/.python-version", "shared/"]
COPY ["agents/.env", "agents/"]

FROM python:3.12-slim
WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY --from=builder /src .

CMD ["/src/.venv/bin/uvicorn", "management_agent.main:app", \
     "--host", "0.0.0.0", "--port", "8000"]





