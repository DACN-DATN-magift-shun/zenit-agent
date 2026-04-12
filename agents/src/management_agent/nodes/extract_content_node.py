from management_agent.prompts.extract_content_prompt import ManagementAgentExtractContentPrompt
from src.utils.llm_util import LLMUtil
from langchain_core.messages import AIMessage, SystemMessage

from management_agent.states.main_state import ManagementAgentMainState


class ManagementAgentExtractContentNode:
    
    @staticmethod
    async def extract_content_from_text(state: ManagementAgentMainState):
        if state["user_confirmation"] is True:
            return {
                "messages": state["messages"],
                "extracted_content": state["extracted_content"]
            }
        
        print(f"Current state messages: {state['messages']}")
            
        llm_model = LLMUtil.get_google_genai_chat_model()
        messages = state["messages"]
        
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [
                SystemMessage(content=ManagementAgentExtractContentPrompt.PROMPT)
            ] + messages
        
        response = await llm_model.ainvoke(messages)
        
        # response đã là AIMessage — dùng trực tiếp, không cần lấy .content[-1]
        if isinstance(response, str):
            response = AIMessage(content=response)
        
        return {
            "messages": state["messages"] + [response],  # ✅ truyền AIMessage object
            "extracted_content": response.content[-1]["text"]
        }