import textwrap

from management_agent.states.main_state import ManagementAgentMainState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

class ManagementAgentUserConfirmationNode:
    @staticmethod
    async def get(state: ManagementAgentMainState):
        user_input = interrupt(textwrap.dedent(f"""{state["extracted_content"]}""").strip())
        
        return {
            "user_confirmation": True if user_input.lower() == "yes" else False
        }
        