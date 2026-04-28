from typing import Any

from pydantic import BaseModel


class ManagementAgentMessageRequest(BaseModel):
    message: str
    conversation_id: str
    # is_interrupted: bool = False
    account_id: str

class ManagementAgentMessageResponse(BaseModel):
    response: Any
    suggestions: Any
    display_accept_button: bool = False
    # is_interrupted: bool = False
    # messages: Any