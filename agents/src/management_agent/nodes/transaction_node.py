import os

from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from management_agent.common.management_env_constants import ManagementAgentEnvConstants
from management_agent.nodes.helpers.extract_content_helper import ManagementAgentExtractContentHelper
from management_agent.tools.category import ManagementAgentCategoryTool
from management_agent.tools.transaction import ManagementAgentTransactionTool
from management_agent.prompts.transaction_prompt import ManagementAgentTransactionPrompt
from management_agent.states.main_state import ManagementAgentMainState
from management_agent.tools.wallet import ManagementAgentWalletTool
from src.common.env_constants import EnvConstants
from src.utils.llm_util import LLMUtil

load_dotenv()

from langchain_core.runnables import RunnableConfig

class ManagementAgentTransactionNode:   
    @staticmethod
    async def create(state: ManagementAgentMainState, config: RunnableConfig):
        llm_model = LLMUtil.get_google_genai_chat_model()
        extracted_content = state["extracted_content"]
        
        llm_model = LLMUtil.get_google_genai_chat_model()
        if state["query"] == "":
            human_messages = [m.content for m in state["messages"] if isinstance(m, HumanMessage)]
            raw_query = "\n".join(human_messages) 
            
            # Rewrite query to be more suitable for vector search
            rewrite_query_invoke = await llm_model.ainvoke([
                SystemMessage(content=[ManagementAgentTransactionPrompt.CREATE_QUERY]),
                HumanMessage(content=raw_query)
            ])
            
            rewrite_query = ManagementAgentExtractContentHelper.extract_text_from_response(rewrite_query_invoke)
            query = rewrite_query
            print(f"Rewritten query for vector search: {rewrite_query}\n================================")
        else:
            query = state["query"]
        
        account_id = config["configurable"]["account_id"]
        tools = [
            ManagementAgentTransactionTool.create(account_id, query), 
            ManagementAgentCategoryTool.get_all(account_id), 
            ManagementAgentWalletTool.get_all(account_id)
        ]
        
        tool_node = ToolNode(tools=tools)
        llm_with_tools = llm_model.bind_tools(tools)
        
        messages = [
            SystemMessage(content=ManagementAgentTransactionPrompt.CREATE_TRANSACTION_PROMPT),
            HumanMessage(content=f"Create transaction from: {extracted_content}")
        ]
        
        all_new_messages = []
        text_response = []

        # ✅ Loop đến khi LLM không còn gọi tool
        while True:
            response = await llm_with_tools.ainvoke(messages)
            all_new_messages.append(response)
            
            if not response.tool_calls:
                text_response.append(ManagementAgentExtractContentHelper.extract_text_from_response(response))
                break
                
            tool_results = await tool_node.ainvoke(
                {"messages": [response]},
                config
            )
            tool_messages = tool_results["messages"]
            all_new_messages.extend(tool_messages)
            messages.extend([response, *tool_messages])

        return {"messages": all_new_messages, "response": "\n".join(text_response)}