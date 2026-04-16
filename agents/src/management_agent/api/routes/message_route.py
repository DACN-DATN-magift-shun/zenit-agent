# message_handler.py
from fastapi import APIRouter, Request
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from management_agent.api.requests.message_request import ManagementAgentMessageRequest, ManagementAgentMessageResponse
from management_agent.nodes.helpers.extract_content_helper import ManagementAgentExtractContentHelper

management_message_router = APIRouter()

class ManagementAgentMessageHandler:
    @staticmethod
    @management_message_router.post("/messages")
    async def create(
        request: ManagementAgentMessageRequest,
        req: Request,
    ) -> ManagementAgentMessageResponse:
        agent = req.app.state.agent
        config = {
            "configurable": {
                "thread_id": request.conversation_id,
                "account_id": request.account_id,
            }
        }

        try:
            current_state = await agent.aget_state(config)
            is_interrupted = any(
                getattr(task, 'interrupts', None)
                for task in (current_state.tasks or [])
                if getattr(task, 'interrupts', None)
            )

            agent_input = (
                Command(resume=request.message)
                if is_interrupted
                else {"messages": [HumanMessage(content=request.message)]}
            )

            async for _ in agent.astream(input=agent_input, config=config):
                pass

            # Lấy state sau khi stream xong — dùng để check interrupt VÀ lấy messages
            updated_state = await agent.aget_state(config)
            serialized_messages = [
                {
                    "role": msg.__class__.__name__,
                    "content": ManagementAgentExtractContentHelper.extract_text_from_response(msg.content),
                    "id": getattr(msg, "id", None),
                }
                for msg in updated_state.values.get("messages", [])
            ]

            # ✅ Check interrupt từ updated_state thay vì track biến riêng
            interrupt_value = next(
                (task.interrupts[0].value for task in (updated_state.tasks or []) if getattr(task, 'interrupts', None)),
                None
            )

            if interrupt_value:
                return ManagementAgentMessageResponse(
                    response=interrupt_value,
                    # messages=serialized_messages,
                )

            return ManagementAgentMessageResponse(
                response=serialized_messages[-1]["content"] if serialized_messages else None,
                # messages=serialized_messages,
            )

        except Exception as e:
            return ManagementAgentMessageResponse(
                response=f"Error: {str(e)}",
                messages=[],
            )