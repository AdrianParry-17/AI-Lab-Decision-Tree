from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Optional
from .distribution import IDistributor
from .forward import IDecisionTreeForwardStrategy, StandardDecisionTreeForwardStrategy
from ...model import IModel

__all__ = [
    'INode', 'IBranchNode', 'DecisionTree',
    'ValueNode', 'FunctionNode', 'DistributorBranchNode'
]

# --- Generic stuff ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class INode(Generic[InputT, OutputT], IModel[InputT, OutputT]):
    pass

class IBranchNode(Generic[InputT, OutputT], INode[InputT, OutputT]):
    @abstractmethod
    def GetDistributor(self) -> IDistributor[InputT, INode[InputT, OutputT]]:
        pass

    def Branch(self, x: InputT) -> INode[InputT, OutputT]:
        return self.GetDistributor().Distribute(x)

    def Execute(self, x: InputT) -> OutputT:
        return self.Branch(x).Execute(x)

class DecisionTree(Generic[InputT, OutputT], IModel[InputT, OutputT]):
    def __init__(
        self,
        root: Optional[INode[InputT, OutputT]] = None,
        forward_strategy: Optional[IDecisionTreeForwardStrategy[InputT, OutputT]] = None
    ) -> None:
        self.__root = root
        self.__forward_strategy = (
            StandardDecisionTreeForwardStrategy()
            if forward_strategy is None
            else forward_strategy
        )

    def Execute(self, x: InputT) -> OutputT:
        if self.__root is None:
            raise RuntimeError('The decision tree has no root!')
        return self.__forward_strategy.Forward(self.__root, x)

    def SetRoot(self, root: Optional[INode[InputT, OutputT]]) -> None:
        self.__root = root

    def GetRoot(self) -> Optional[INode[InputT, OutputT]]:
        return self.__root

    def SetForwardStrategy(self, forward_strategy: IDecisionTreeForwardStrategy[InputT, OutputT]) -> None:
        if forward_strategy is None:
            raise ValueError('[forward_strategy] cannot be None!')
        self.__forward_strategy = forward_strategy

    def GetForwardStrategy(self) -> IDecisionTreeForwardStrategy[InputT, OutputT]:
        return self.__forward_strategy

# --- Specific stuff ---

@dataclass
class ValueNode(Generic[InputT, OutputT], INode[InputT, OutputT]):
    Output: OutputT

    def Execute(self, x: InputT) -> OutputT:
        return self.Output

class FunctionNode(Generic[InputT, OutputT], INode[InputT, OutputT]):
    def __init__(self, function: Callable[[InputT], OutputT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function: Callable[[InputT], OutputT] = function

    def Execute(self, x: InputT) -> OutputT:
        return self.Function(x)

class DistributorBranchNode(Generic[InputT, OutputT], IBranchNode[InputT, OutputT]):
    def __init__(self, distributor: IDistributor[InputT, INode[InputT, OutputT]]) -> None:
        if distributor is None:
            raise ValueError('[distributor] cannot be None!')
        self.__distributor = distributor

    def GetDistributor(self) -> IDistributor[InputT, INode[InputT, OutputT]]:
        return self.__distributor
