from langgraph.graph import END, START, StateGraph

from management_agent.nodes.extract_content_node import ManagementAgentExtractContentNode
from management_agent.nodes.handle_missing_fields_node import ManagementAgentHandleMissingFieldsNode
from management_agent.nodes.transaction_node import ManagementAgentTransactionNode
from management_agent.nodes.user_confirmation_node import ManagementAgentUserConfirmationNode
from management_agent.states.main_state import ManagementAgentMainState
from src.graphs.graph_base import BaseGraph


class ManagementAgentMainGraph(BaseGraph):
    def __init__(self, checkpointer, store):
        super().__init__(checkpointer, store)
        
    def build_state_graph(self):
        graph = StateGraph(ManagementAgentMainState)
        
        # Add nodes
        graph.add_node("extract_content", ManagementAgentExtractContentNode.extract_content_from_text)
        graph.add_node("clean_suggestions", ManagementAgentUserConfirmationNode.clean_missing_fields_suggestions)
        graph.add_node("user_confirmation", ManagementAgentUserConfirmationNode.get_transaction_confirmation)
        graph.add_node("user_confirmation_missing_fields", ManagementAgentUserConfirmationNode.get_missing_fields_confirmation)
        graph.add_node("handle_missing_fields", ManagementAgentHandleMissingFieldsNode.handle_missing_fields)
        graph.add_node("create_transaction", ManagementAgentTransactionNode.create)
        
        # Add edges
        graph.add_edge(START, "extract_content")
        graph.add_conditional_edges(
            "extract_content",
            self._is_missing_fields,
            {
                True: "handle_missing_fields",
                False: "clean_suggestions"
            }
        )
        graph.add_edge("handle_missing_fields", "user_confirmation_missing_fields")
        graph.add_edge("user_confirmation_missing_fields", "extract_content")
        graph.add_edge("clean_suggestions", "user_confirmation")
        
        graph.add_conditional_edges(
            "user_confirmation",
            self._is_user_confirmation,
            {
                True: "create_transaction",
                False: END
            }   
        )
        graph.add_edge("create_transaction", END)
        
        
        return graph.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )
    
    def _is_missing_fields(self, state: ManagementAgentMainState):
        missing_fields = state["missing_fields"]
        print(f"Current missing fields in _is_missing_fields: {missing_fields}\n===============================")
        
        return len(missing_fields) > 0
    
    def _is_user_confirmation(self, state: ManagementAgentMainState):
        return True if state["user_confirmation"] else False