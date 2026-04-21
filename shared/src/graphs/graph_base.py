from abc import ABC, abstractmethod
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver

from src.graphs.i_graph import IGraph

Checkpointer = MemorySaver | PostgresSaver
Store = InMemoryStore | PostgresStore


class BaseGraph(IGraph, ABC):
    def __init__(self, checkpointer: Checkpointer, store: Store):
        self.checkpointer = checkpointer
        self.store = store

    @abstractmethod
    def build_state_graph(self):
        pass