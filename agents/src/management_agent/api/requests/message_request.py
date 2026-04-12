from typing import Any

from pydantic import BaseModel


class ManagementAgentMessageRequest(BaseModel):
    message: str
    thread_id: str = "default"

class ManagementAgentMessageResponse(BaseModel):
    response: Any
    is_interrupted: bool = False