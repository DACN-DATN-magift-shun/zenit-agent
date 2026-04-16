import textwrap

from management_agent.states.main_state import ManagementAgentMainState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

class ManagementAgentUserConfirmationNode:
    @staticmethod
    async def get(state: ManagementAgentMainState):
        user_input = interrupt(textwrap.dedent(f"""
            Bạn hãy xác nhận lại thông tin giao dịch mà bạn vừa cung cấp giúp tôi nhé!
            {state["extracted_content"]}
            Nếu có sai sót gì thì bạn hãy cho tôi biết nhé!
        """).strip())
        
        return {
            "user_confirmation": True if user_input.lower() == "yes" else False
        }
        