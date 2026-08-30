from abc import ABC, abstractmethod
from typing import TypeVar, Generic

__all__ = ['IModel']

# --- Generic stuff ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class IModel(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def Execute(self, x: InputT) -> OutputT:
        pass

# --- Specific stuff will be here... probably ---
