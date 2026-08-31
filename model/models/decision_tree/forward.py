from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable
from ...model import IModel

__all__ = [
    'IDecisionTreeForwardStrategy',
    'StandardDecisionTreeForwardStrategy',
    'FunctionDecisionTreeForwardStrategy'
]

# --- Generic stuff ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class IDecisionTreeForwardStrategy(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def Forward(self, root: IModel[InputT, OutputT], x: InputT) -> OutputT:
        pass

# --- Specific stuff ---

class StandardDecisionTreeForwardStrategy(Generic[InputT, OutputT], IDecisionTreeForwardStrategy[InputT, OutputT]):
    def Forward(self, root: IModel[InputT, OutputT], x: InputT) -> OutputT:
        return root.Execute(x)

class FunctionDecisionTreeForwardStrategy(Generic[InputT, OutputT], IDecisionTreeForwardStrategy[InputT, OutputT]):
    def __init__(self, function: Callable[[IModel[InputT, OutputT], InputT], OutputT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Forward(self, root: IModel[InputT, OutputT], x: InputT) -> OutputT:
        return self.Function(root, x)
