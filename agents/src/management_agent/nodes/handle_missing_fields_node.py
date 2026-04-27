import os

from dotenv import load_dotenv
from management_agent.api.data.management_qdrant import ManagementAgentQdrant
from management_agent.common.management_qdrant_constants import ManagementAgentQdrantConstants
from management_agent.nodes.helpers.extract_content_helper import ManagementAgentExtractContentHelper
from management_agent.prompts.handle_missing_fields_prompt import ManagementAgentHandleMissingFieldsPrompt
from management_agent.states.main_state import ManagementAgentMainState
from qdrant_client import QdrantClient
from src.common.env_constants import EnvConstants
from src.data.requests.qdrant_search_request import QdrantSearchRequest
from src.utils.llm_util import LLMUtil
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.types import interrupt
from langchain_core.runnables import RunnableConfig
load_dotenv()


class ManagementAgentHandleMissingFieldsNode:
    @staticmethod
    async def handle_missing_fields(state: ManagementAgentMainState, config: RunnableConfig):
        missing_fields = state['missing_fields']
        print(f"Missing fields value in handle_missing_fields node: {missing_fields}\n===============================")
        
        llm_model = LLMUtil.get_google_genai_chat_model()
        rewrite_query = None
        search_results = None
        extracted_suggestions = []
        
        if any(f in missing_fields for f in ["transaction_date", "amount", "title"]):
            print("Python running in this block - transaction_date, amount, title\n===============================")
            return {
                "suggestions": extracted_suggestions
            }
            
        # Handle optional fields that can be suggested or requested
        if any(f in missing_fields for f in ["category", "wallet"]):
            print("Python running in this block - category, wallet\n===============================")
            qdrant_client = QdrantClient(url=os.getenv(EnvConstants.QDRANT_CLIENT_URL))
            qdrant = ManagementAgentQdrant(qdrant_client)
            
            # Get all human messages
            human_messages = [m.content for m in state["messages"] if isinstance(m, HumanMessage)]
            raw_query = "\n".join(human_messages) 
            
            # Rewrite query to be more suitable for vector search
            rewrite_query_invoke = await llm_model.ainvoke([
                SystemMessage(content=[ManagementAgentHandleMissingFieldsPrompt.REWRITE_QUERY]),
                HumanMessage(content=raw_query)
            ])
            
            rewrite_query = ManagementAgentExtractContentHelper.extract_text_from_response(rewrite_query_invoke)
            print(f"Rewritten query for vector search: {rewrite_query}\n================================")
            
            # Search in Qdrant using the rewritten query vector
            search_results = qdrant.search(
                QdrantSearchRequest(
                    collection="transactions",
                    query=rewrite_query,
                    account_id=config["configurable"]["account_id"]
                )
            )
            print(f"Qdrant search results: {search_results}\n================================")
            
            if search_results:
                extracted_suggestions = ManagementAgentExtractContentHelper.extract_qdrant_search_results(search_results.points)
            #     # state["suggestions"] = extracted_suggestions
            #     interrupt_message = f"Tôi nhận thấy bạn đang thiếu các trường **{', '.join([f for f in missing_fields if f in ['category', 'wallet']])}**. Dựa trên những gì bạn đã nói, tôi gợi ý các giá trị sau cho các trường này. Bạn hãy lựa chọn các giá trị này hoặc cung cấp giá trị cho các trường này giúp tôi nhé!"
            else:
            #     interrupt_message = f"Tôi nhận thấy bạn đang thiếu các trường **{', '.join([f for f in missing_fields if f in ['category', 'wallet']])}**. Bạn hãy cung cấp giá trị cho các trường này giúp tôi nhé!"
                extracted_suggestions = []
                
            print(f"Suggestions: {extracted_suggestions}\n================================")
            return {
                "query": rewrite_query,
                "suggestions": extracted_suggestions
            }