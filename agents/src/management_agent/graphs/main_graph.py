from langgraph.graph import END, START, StateGraph

from management_agent.nodes.extract_content_node import ManagementAgentExtractContentNode
from management_agent.nodes.transaction_node import ManagementAgentTransactionNode
from management_agent.states.main_state import ManagementAgentMainState
from src.graphs.graph_base import BaseGraph


class ManagementAgentMainGraph(BaseGraph):
    def __init__(self, checkpointer, store):
        super().__init__(checkpointer, store)
        
    def build_state_graph(self):
        graph = StateGraph(ManagementAgentMainState)
        
        graph.add_node("extract_content", ManagementAgentExtractContentNode.extract_content_from_text)
        graph.add_node("create_transaction", ManagementAgentTransactionNode.create)
        
        graph.add_edge(START, "extract_content")
        graph.add_conditional_edges("extract_content", 
            lambda state: "create_transaction" if state["user_confirmation"] else "extract_content"
        )
        graph.add_edge("create_transaction", END)
        
        return graph.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )