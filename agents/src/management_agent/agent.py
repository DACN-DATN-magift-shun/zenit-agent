import os
from dotenv import load_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.graphs.main_graph import ManagementAgentMainGraph
from psycopg_pool import AsyncConnectionPool

load_dotenv()

class ManagementAgent:
    def __init__(self, checkpointer, store):
        self.graph = ManagementAgentMainGraph(
            checkpointer=checkpointer,
            store=store,
        ).build_state_graph()


async def get_agent():
    db_url = os.getenv(ManagementAgentEnvConstants.MANAGEMENT_POSTGRES_URL)
    
    pool_kwargs = {
        "autocommit": True,
        "connect_timeout": 30,
        "options": "-c statement_timeout=60000 -c idle_in_transaction_session_timeout=120000"
    }
    
    checkpointer_pool = AsyncConnectionPool(
        conninfo=db_url,
        min_size=1,
        max_size=10,
        kwargs=pool_kwargs
    )
    await checkpointer_pool.open()
    
    store_pool = AsyncConnectionPool(
        conninfo=db_url,
        min_size=1,
        max_size=10,
        kwargs=pool_kwargs
    )
    await store_pool.open()
    
    checkpointer = AsyncPostgresSaver(checkpointer_pool)
    await checkpointer.setup()
    print("Checkpointer setup complete")
    
    store = AsyncPostgresStore(store_pool)
    await store.setup()
    print("Store setup complete")
    
    agent = ManagementAgent(checkpointer, store)
    return agent.graph