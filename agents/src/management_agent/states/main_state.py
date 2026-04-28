from typing import Any, Dict, List, Optional

from src.states.state_base import BaseState


class ManagementAgentMainState(BaseState):
    missing_fields: Optional[List[str]]
    query: Optional[str]
    extracted_content: Optional[Any]
    display_accept_button: Optional[bool]
    user_confirmation: Optional[Any]
    suggestions: Optional[List[Any]]
    
    