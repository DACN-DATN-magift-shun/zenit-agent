from management_agent.states.main_state import ManagementAgentMainState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

class ManagementAgentConfirmNode:
    @staticmethod
    def get_user_confirmation(state: ManagementAgentMainState):
        # 1. Gọi interrupt và hứng giá trị phản hồi từ UI/Người dùng
        # Khi node này chạy lần đầu, nó sẽ dừng tại đây.
        # Khi người dùng nhấn "Submit" trên UI, giá trị đó sẽ được trả về vào biến confirmation_input
        confirmation_input = interrupt(
            f"Please confirm if you want to proceed with the following content: {state.get('extracted_content')}"
        )
        
        # 2. Xử lý giá trị nhận được từ interrupt
        # Giả sử confirmation_input là một string hoặc dict tùy bạn cấu hình ở Front-end
        user_reply = str(confirmation_input).lower().strip()
        
        is_confirmed = user_reply in ["yes", "y", "confirm", "proceed"]
        
        # 3. Trả về state mới
        return {
            "user_confirmation": is_confirmed,
            "messages": [HumanMessage(content=str(confirmation_input))]
        }