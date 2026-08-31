from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from .objective import IObjective

__all__ = ['IOptimizer']

# --- Generic stuff ---

InputStateT = TypeVar('InputStateT')
OutputStateT = TypeVar('OutputStateT')
ObjectiveT = TypeVar('ObjectiveT', bound=IObjective[Any, Any])

class IOptimizer(ABC, Generic[InputStateT, OutputStateT, ObjectiveT]):
    @abstractmethod
    def Optimize(self, state: InputStateT, objective: ObjectiveT) -> OutputStateT:
        pass

# --- Specific stuff here... i guess ---
