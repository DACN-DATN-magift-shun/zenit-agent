# message_handler.py
import time
import logging

from fastapi import APIRouter, Request
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from management_agent.api.requests.message_request import ManagementAgentMessageRequest, ManagementAgentMessageResponse
from management_agent.nodes.helpers.extract_content_helper import ManagementAgentExtractContentHelper

logger = logging.getLogger(__name__)
management_message_router = APIRouter()

class ManagementAgentMessageHandler:
    @staticmethod
    @management_message_router.post("/messages")
    async def create(
        request: ManagementAgentMessageRequest,
        req: Request,
    ) -> ManagementAgentMessageResponse:
        start_time = time.time()
        
        agent = req.app.state.agent
        config = {
            "configurable": {
                "thread_id": request.conversation_id,
                "account_id": request.account_id,
            }
        }

        try:
            # ⏱️ Measure 1: Get current state
            t1 = time.time()
            current_state = await agent.aget_state(config)
            print(f"Get current state: {time.time() - t1:.2f}s")
            
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

            # ⏱️ Measure 2: Agent stream (usually the slowest part)
            t2 = time.time()
            async for _ in agent.astream(input=agent_input, config=config):
                pass
            print(f"Agent stream: {time.time() - t2:.2f}s")

            # ⏱️ Measure 3: Get updated state
            t3 = time.time()
            updated_state = await agent.aget_state(config)
            print(f"Get updated state: {time.time() - t3:.2f}s")
            
            # ⏱️ Measure 4: Serialize messages
            t4 = time.time()
            serialized_messages = [
                {
                    "role": msg.__class__.__name__,
                    "content": ManagementAgentExtractContentHelper.extract_text_from_response(msg.content),
                    "id": getattr(msg, "id", None),
                }
                for msg in updated_state.values.get("messages", [])
            ]
            print(f"Serialize messages: {time.time() - t4:.2f}s")

            interrupt_value = next(
                (task.interrupts[0].value for task in (updated_state.tasks or []) if getattr(task, 'interrupts', None)),
                None
            )
            
            response_time = time.time() - start_time
            print(f"--- Total Response time: {response_time:.2f}s ---")

            if interrupt_value:
                return ManagementAgentMessageResponse(
                    response=interrupt_value,
                    suggestions=updated_state.values.get("suggestions", []),
                    display_accept_button=updated_state.values.get("display_accept_button", False),
                )

            return ManagementAgentMessageResponse(
                response=serialized_messages[-1]["content"] if serialized_messages else None,
                suggestions=updated_state.values.get("suggestions", []),
                display_accept_button=updated_state.values.get("display_accept_button", False),
            )

        except Exception as e:
            print(f"Error: {str(e)}")
            return ManagementAgentMessageResponse(
                response=f"Error: {str(e)}",
                suggestions=[],
                display_accept_button=False,
            )