from typing import TypedDict
import uuid

from langgraph.graph import add_messages
from typing_extensions import Annotated


class BaseState(TypedDict):
    messages: Annotated[list, add_messages]
    account_id: str
    thread_id: str