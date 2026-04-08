from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from management_agent.graphs.main_graph import ManagementAgentMainGraph


class ManagementAgent:
    def __init__(self):
        self.graph = ManagementAgentMainGraph(
            checkpointer=MemorySaver(), 
            store=InMemoryStore()
        ).build_state_graph()
        
        self.config = {
            "configurable": {
                "thread_id": "default"
            }
        }
        
    
    def run(self, user_message: str):
        result = self.graph.invoke(
            {"messages": [ {"role": "user", "content": user_message} ]},
            config=self.config
        )
        
        return result["messages"][-1].content

def get_agent():
    agent = ManagementAgent()
    return agent.graph