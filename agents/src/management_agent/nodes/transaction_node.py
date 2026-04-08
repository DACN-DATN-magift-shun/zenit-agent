from langchain_core.messages import AIMessage

from management_agent.states.main_state import ManagementAgentMainState


class ManagementAgentTransactionNode:   
    @staticmethod
    def create(state: ManagementAgentMainState):
        return {
            "messages": [
                AIMessage(content="Transaction has been created successfully!")
            ]
        }