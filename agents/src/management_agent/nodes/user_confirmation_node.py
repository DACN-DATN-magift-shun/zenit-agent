from management_agent.states.main_state import ManagementAgentMainState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

class ManagementAgentUserConfirmationNode:
    @staticmethod
    async def get(state: ManagementAgentMainState):
        user_input = interrupt("""
            Bạn hãy xác nhận lại thông tin giao dịch mà bạn vừa cung cấp giúp tôi nhé!
            Nếu có sai sót gì thì bạn hãy sửa lại giúp tôi luôn nhé!      
        """)
        
        return {
            "user_confirmation": True if user_input.lower() == "yes" else False
        }
        