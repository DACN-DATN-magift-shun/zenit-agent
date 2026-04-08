from typing import Any, Dict, List

from src.states.state_base import BaseState


class ManagementAgentMainState(BaseState):
    extracted_content: Dict[str, Any] | List[Dict[str, Any]] = None
    user_confirmation: bool = False