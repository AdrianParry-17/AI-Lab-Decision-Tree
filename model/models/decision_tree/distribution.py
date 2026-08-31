from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable
from .split import ISplit
from .mapping import IBranchMapping

__all__ = [
    'IDistributor', 'FunctionDistributor', 'SplitDistributor'
]

# --- Generic stuff ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
BranchT = TypeVar('BranchT')

class IDistributor(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def Distribute(self, x: InputT) -> OutputT:
        pass

# --- Specific stuff ---

class FunctionDistributor(Generic[InputT, OutputT], IDistributor[InputT, OutputT]):
    def __init__(self, function: Callable[[InputT], OutputT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function: Callable[[InputT], OutputT] = function

    def Distribute(self, x: InputT) -> OutputT:
        return self.Function(x)

class SplitDistributor(Generic[InputT, BranchT, OutputT], IDistributor[InputT, OutputT]):
    def __init__(
        self,
        split: ISplit[InputT, BranchT],
        mapping: IBranchMapping[BranchT, OutputT]
    ) -> None:
        if split is None:
            raise ValueError('[split] cannot be None!')
        if mapping is None:
            raise ValueError('[mapping] cannot be None!')

        self.__split = split
        self.__mapping = mapping

    def GetSplit(self) -> ISplit[InputT, BranchT]:
        return self.__split

    def GetMapping(self) -> IBranchMapping[BranchT, OutputT]:
        return self.__mapping

    def Distribute(self, x: InputT) -> OutputT:
        return self.__mapping.Map(self.__split.Split(x))
