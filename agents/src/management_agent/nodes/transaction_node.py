import os

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.tools.transaction import ManagementAgentTransactionTool
from management_agent.prompts.transaction_prompt import ManagementAgentParseContentPrompt
from management_agent.states.main_state import ManagementAgentMainState
from src.common.env_constants import EnvConstants
from src.utils.llm_util import LLMUtil

class ManagementAgentTransactionNode:   
    @staticmethod
    async def create(state: ManagementAgentMainState):
        llm_model = LLMUtil.get_google_genai_chat_model()
        extracted_content = state["extracted_content"]
        
        # Bind tool vào model
        tools = [ManagementAgentTransactionTool.create]
        llm_with_tools = llm_model.bind_tools(tools)
        
        print(f"Extracted content to parse: {extracted_content}")
        
        response = await llm_with_tools.ainvoke([
            SystemMessage(content=ManagementAgentParseContentPrompt.CREATE_TRANSACTION_PROMPT),
            HumanMessage(content=f"Create transaction from: {extracted_content}")
        ])
        
        print(f"API URL: {os.getenv(ManagementAgentEnvConstants.MANAGEMENT_API_BASE_URL)}/Transactions")
        
        # Xử lý tool calls từ response
        if response.tool_calls:
            tool_results = []
            for tool_call in response.tool_calls:
                print(f"Tool called: {tool_call['name']}")
                if tool_call["name"] == "create":
                    result = await ManagementAgentTransactionTool.create.ainvoke(tool_call["args"])
                    tool_results.append(result)
            
            return {"messages": [AIMessage(content=f"Created {len(tool_results)} transaction(s)!")]}
        
        return {"messages": [AIMessage(content=response.content if hasattr(response, 'content') else str(response))]}