from dotenv import load_dotenv
from management_agent.nodes.helpers.extract_content_helper import ManagementAgentExtractContentHelper
from management_agent.prompts.extract_content_prompt import ManagementAgentExtractContentPrompt
from management_agent.tools.transaction import ManagementAgentTransactionTool
from src.utils.llm_util import LLMUtil
from langchain_core.messages import AIMessage, SystemMessage

from management_agent.states.main_state import ManagementAgentMainState

load_dotenv()


class ManagementAgentExtractContentNode:  
    @staticmethod
    async def extract_content_from_text(state: ManagementAgentMainState):
        tools = [ManagementAgentTransactionTool.get_missing_fields]
        llm_model = LLMUtil.get_google_genai_chat_model().bind_tools(tools)
        messages = state["messages"]
        
        messages = [
            SystemMessage(content=ManagementAgentExtractContentPrompt.PROMPT)
        ] + messages
        
        response = await llm_model.ainvoke(messages)
        text_response = ManagementAgentExtractContentHelper.extract_text_from_response(response)
        print(f"Text response from LLM: {text_response}\n===============================")

        tool_results = []
        missing_fields = []
        
        for tool_call in response.tool_calls:
            if tool_call["name"] == "get_missing_fields":
                result = await ManagementAgentTransactionTool.get_missing_fields.ainvoke(tool_call["args"])
                missing_fields = result  
            else:
                result = None
            tool_results.append(result)
        print(f"Tool call results: {tool_results}\n===============================")

        return {
            "messages": [text_response] if text_response else [],
            "extracted_content": text_response if text_response else "",
            "missing_fields": missing_fields,
            "query": ""
        }