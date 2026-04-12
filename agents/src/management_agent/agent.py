import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.graphs.main_graph import ManagementAgentMainGraph
import psycopg

load_dotenv()


class ManagementAgent:
    def __init__(self, checkpointer, store):
        self.graph = ManagementAgentMainGraph(
            checkpointer=checkpointer,
            store=store
        ).build_state_graph()
        
    
    # def run(self, user_message: str):
    #     result = self.graph.invoke(
    #         {"messages": [ {"role": "user", "content": user_message} ]},
    #     )
        
    #     return result["messages"][-1].content

async def get_agent():
    conn = await psycopg.AsyncConnection.connect(
        os.getenv(ManagementAgentEnvConstants.MANAGEMENT_POSTGRES_URL),
        autocommit=True
    )
    
    print("Connected to Postgres")
    
    checkpointer = AsyncPostgresSaver(conn)
    await checkpointer.setup()
    
    print("Checkpointer setup complete")
    
    store = AsyncPostgresStore(conn)
    await store.setup()
    
    print("Store setup complete")
    
    agent = ManagementAgent(checkpointer, store)
    return agent.graph