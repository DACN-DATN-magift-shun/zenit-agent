import textwrap

from management_agent.states.main_state import ManagementAgentMainState
from langgraph.types import interrupt
from langchain_core.messages import HumanMessage

class ManagementAgentUserConfirmationNode:
    @staticmethod
    async def clean_missing_fields_suggestions(state: ManagementAgentMainState):
        return {
            "suggestions": []
        }
        
    @staticmethod
    async def get_transaction_confirmation(state: ManagementAgentMainState):
        user_input = interrupt(textwrap.dedent(f"""{state["extracted_content"]}""").strip())
        
        return {
            "user_confirmation": True if user_input.lower() == "yes" else False,
        }
    
    @staticmethod
    async def get_missing_fields_confirmation(state: ManagementAgentMainState):
        suggestions = state["suggestions"]
        missing_fields = state['missing_fields']
        
        if any(f in missing_fields for f in ["transaction_date", "amount", "title"]):
            interrupt_message = f"""Tôi nhận thấy bạn đang thiếu các trường **{', '.join([f for f in missing_fields if f in ['transaction_date', 'amount', 'title']])}**. Bạn hãy cung cấp giá trị cho các trường này giúp tôi nhé!"""
        elif any(f in missing_fields for f in ["category", "wallet"]):
            if suggestions != []:
                interrupt_message = f"Tôi nhận thấy bạn đang thiếu các trường **{', '.join([f for f in missing_fields if f in ['category', 'wallet']])}**. Dựa trên những gì bạn đã nói, tôi gợi ý các giá trị sau cho các trường này. Bạn hãy lựa chọn các giá trị này hoặc cung cấp giá trị cho các trường này giúp tôi nhé!"
            else:
                interrupt_message = f"Tôi nhận thấy bạn đang thiếu các trường **{', '.join([f for f in missing_fields if f in ['category', 'wallet']])}**. Bạn hãy cung cấp giá trị cho các trường này giúp tôi nhé!"
        
        user_input = interrupt(interrupt_message)
        return {
            "messages": [HumanMessage(content=user_input)],
            "suggestions": suggestions
        }
        