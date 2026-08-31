from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Any
from ..data import IData

__all__ = [
    'IObjective',  'FunctionObjective', 'IDataObjective',
    'IValueDataObjective', 'FunctionValueDataObjective'
]

# --- Generic stuff ---

OutputT = TypeVar('OutputT')
EvaluateT = TypeVar('EvaluateT')

class IObjective(ABC, Generic[OutputT, EvaluateT]):
    @abstractmethod
    def Evaluate(self, output: OutputT) -> EvaluateT:
        pass

class FunctionObjective(Generic[OutputT, EvaluateT], IObjective[OutputT, EvaluateT]):
    def __init__(self, function: Callable[[OutputT], EvaluateT]) -> None:
        if function is None:
            raise ValueError("[function] cannot be None!")
        self.Function: Callable[[OutputT], EvaluateT] = function

    def Evaluate(self, output: OutputT) -> EvaluateT:
        return self.Function(output)

# Bridge to IData

ObjectiveDataT = TypeVar('ObjectiveDataT', bound=IData[Any])

class IDataObjective(Generic[OutputT, EvaluateT, ObjectiveDataT], IObjective[OutputT, EvaluateT]):
    @abstractmethod
    def GetData(self) -> ObjectiveDataT:
        pass

# --- Specific stuff ---

@dataclass
class IValueDataObjective(Generic[OutputT, EvaluateT, ObjectiveDataT], IDataObjective[OutputT, EvaluateT, ObjectiveDataT]):
    Data: ObjectiveDataT

    def GetData(self) -> ObjectiveDataT:
        return self.Data

class FunctionValueDataObjective(Generic[OutputT, EvaluateT, ObjectiveDataT], IValueDataObjective[OutputT, EvaluateT, ObjectiveDataT]):
    def __init__(self, data: ObjectiveDataT, function: Callable[[OutputT], EvaluateT]) -> None:
        if function is None:
            raise ValueError("[function] cannot be None!")
        super().__init__(data)
        self.Function: Callable[[OutputT], EvaluateT] = function

    def Evaluate(self, output: OutputT) -> EvaluateT:
        return self.Function(output)
