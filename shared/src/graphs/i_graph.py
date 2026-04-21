from abc import ABC, abstractmethod


class IGraph(ABC):
    @abstractmethod
    def build_state_graph(self):
        pass