from management_agent.prompts.extract_content_prompt import ManagementAgentExtractContentPrompt
from src.utils.llm_util import LLMUtil
from langchain_core.messages import AIMessage, SystemMessage

from management_agent.states.main_state import ManagementAgentMainState


class ManagementAgentExtractContentNode:
    
    @staticmethod
    def extract_content_from_text(state: ManagementAgentMainState):
        llm_model = LLMUtil.get_google_genai_model()
        messages = state["messages"]
        
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [
                SystemMessage(content=ManagementAgentExtractContentPrompt.PROMPT)
            ] + messages
        
        response = llm_model.invoke(messages)
        
        # If response is already a message object, use it directly
        if isinstance(response, str):
            response = AIMessage(content=response)
        
        return {
            "messages": state["messages"] + [response.content[-1]],
            "extracted_content": response.content[-1]
        }
    
    