from langchain_core.messages import AIMessage

from management_agent.states.main_state import ManagementAgentMainState
from src.utils.llm_util import LLMUtil


class ManagementAgentTransactionNode:   
    @staticmethod
    def create(state: ManagementAgentMainState):
        llm_model = LLMUtil.get_google_genai_model()
        extracted_content = state["extracted_content"]
        
        return {
            "messages": [
                AIMessage(content="Transaction has been created successfully!")
            ]
        }