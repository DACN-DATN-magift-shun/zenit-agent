from dotenv import load_dotenv
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
        
        if isinstance(response, str):
            response = AIMessage(content=response)

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
            "messages": [response],
            "extracted_content": response.content,
            "missing_fields": missing_fields,
            "query": ""
        }