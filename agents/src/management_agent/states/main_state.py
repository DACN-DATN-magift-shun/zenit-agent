from typing import Any, Dict, List, Optional

from src.states.state_base import BaseState


class ManagementAgentMainState(BaseState):
    vector_query: Optional[str]
    extracted_content: Dict[str, Any] | List[Dict[str, Any]] = None
    user_confirmation: bool = False
    missing_fields: List[str] = []
    
    