from fastapi import APIRouter, Request
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from management_agent.agent import ManagementAgent, get_agent
from management_agent.api.requests.message_request import ManagementAgentMessageRequest, ManagementAgentMessageResponse

management_message_router = APIRouter()

# Mai hãy tập viết lại hàm create
class ManagementAgentMessageHandler:
    @staticmethod
    @management_message_router.post("/messages")
    async def create(request: ManagementAgentMessageRequest, req: Request) -> ManagementAgentMessageResponse:
        management_agent = req.app.state.agent
        config = {
            "configurable": {
                "thread_id": request.thread_id,
            }
        }
        
        try:
            user_confirmation = True if request.message.lower() == "yes" else False
            
            print("User confirmation:", user_confirmation)
            
            if user_confirmation:
                response = await management_agent.ainvoke(
                    input={
                        "messages": [HumanMessage(content=request.message)],
                        "user_confirmation": True
                    },
                    config=config
                )
            else:
                response = await management_agent.ainvoke(
                    input={
                        "messages": [HumanMessage(content=request.message)],
                        "user_confirmation": False,
                    },
                    config=config,
                    interrupt_after=["extract_content"]
                )
                
            return ManagementAgentMessageResponse(response=response, is_interrupted=False)            
                             
        except Exception as e:
            return ManagementAgentMessageResponse(response=f"Error: {str(e)}")