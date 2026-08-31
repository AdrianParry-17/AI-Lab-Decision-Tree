from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable, Optional, Sequence, Tuple, Iterable
from ...train.training_strategy import ITrainingStrategy
from ...train.objective import IObjective
from .tree import DecisionTree, INode, ValueNode, DistributorBranchNode
from .split import ISplit
from .mapping import (
    IInspectableBranchMapping,
    IBranchMappingBuilder, ListBranchMapping, ListBranchMappingBuilder
)
from .distribution import SplitDistributor
from .objective import IObjectiveBuilder
from .optimizer import ISplitOptimizer, NoSplitCandidateError

__all__ = [
    'IDecisionTreeTrainingStrategy',
    'DecisionTreeNodeTrainingState',
    'IStoppingCriterion', 'FunctionStoppingCriterion',
    'AnyStoppingCriterion', 'MaxDepthStoppingCriterion', 'MinDataStoppingCriterion',
    'ILeafBuilder', 'FunctionLeafBuilder',
    'SupervisedMajorityLeafBuilder', 'SupervisedMeanLeafBuilder',
    'ISplitPartitioner', 'FunctionSplitPartitioner', 'InputSplitPartitioner',
    'RecursiveGreedyDecisionTreeTrainingStrategy'
]

# --- Generic stuff ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
DataT = TypeVar('DataT')
BranchT = TypeVar('BranchT')
EvaluateT = TypeVar('EvaluateT')
StateT = TypeVar('StateT')

class IDecisionTreeTrainingStrategy(
    Generic[InputT, OutputT],
    ITrainingStrategy[DecisionTree[InputT, OutputT]]
):
    pass

@dataclass(frozen=True)
class DecisionTreeNodeTrainingState(Generic[DataT]):
    Data: Sequence[DataT]
    Depth: int = 0

class IStoppingCriterion(ABC, Generic[StateT]):
    @abstractmethod
    def ShouldStop(self, state: StateT) -> bool:
        pass

class ILeafBuilder(ABC, Generic[DataT, InputT, OutputT]):
    @abstractmethod
    def Build(self, data: Sequence[DataT]) -> INode[InputT, OutputT]:
        pass

class ISplitPartitioner(ABC, Generic[DataT, InputT, BranchT]):
    @abstractmethod
    def Partition(
        self,
        data: Sequence[DataT],
        split: ISplit[InputT, BranchT]
    ) -> IInspectableBranchMapping[BranchT, Sequence[DataT]]:
        pass

# --- Specific stuff ---

class FunctionStoppingCriterion(Generic[StateT], IStoppingCriterion[StateT]):
    def __init__(self, function: Callable[[StateT], bool]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def ShouldStop(self, state: StateT) -> bool:
        return self.Function(state)

class AnyStoppingCriterion(Generic[StateT], IStoppingCriterion[StateT]):
    def __init__(self, criteria: Iterable[IStoppingCriterion[StateT]]) -> None:
        if criteria is None:
            raise ValueError('[criteria] cannot be None!')
        self.Criteria = tuple(criteria)

    def ShouldStop(self, state: StateT) -> bool:
        return any(criterion.ShouldStop(state) for criterion in self.Criteria)

class MaxDepthStoppingCriterion(Generic[DataT], IStoppingCriterion[DecisionTreeNodeTrainingState[DataT]]):
    def __init__(self, max_depth: int) -> None:
        if max_depth < 0:
            raise ValueError('[max_depth] must be non-negative!')
        self.MaxDepth = max_depth

    def ShouldStop(self, state: DecisionTreeNodeTrainingState[DataT]) -> bool:
        return state.Depth >= self.MaxDepth

class MinDataStoppingCriterion(Generic[DataT], IStoppingCriterion[DecisionTreeNodeTrainingState[DataT]]):
    def __init__(self, min_data: int) -> None:
        if min_data < 1:
            raise ValueError('[min_data] must be at least 1!')
        self.MinData = min_data

    def ShouldStop(self, state: DecisionTreeNodeTrainingState[DataT]) -> bool:
        return len(state.Data) <= self.MinData

class FunctionLeafBuilder(Generic[DataT, InputT, OutputT], ILeafBuilder[DataT, InputT, OutputT]):
    def __init__(self, function: Callable[[Sequence[DataT]], INode[InputT, OutputT]]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Build(self, data: Sequence[DataT]) -> INode[InputT, OutputT]:
        return self.Function(data)

class SupervisedMajorityLeafBuilder(Generic[DataT, InputT, OutputT], ILeafBuilder[DataT, InputT, OutputT]):
    def __init__(self, output_getter: Callable[[DataT], OutputT]) -> None:
        if output_getter is None:
            raise ValueError('[output_getter] cannot be None!')
        self.OutputGetter = output_getter

    def Build(self, data: Sequence[DataT]) -> INode[InputT, OutputT]:
        if len(data) == 0:
            raise ValueError('Cannot build a majority leaf from empty data!')

        counts: list[Tuple[OutputT, int]] = []

        for item in data:
            output = self.OutputGetter(item)
            found = False

            for i, (current, count) in enumerate(counts):
                if current == output:
                    counts[i] = (current, count + 1)
                    found = True
                    break

            if not found:
                counts.append((output, 1))

        best_output = counts[0][0]
        best_count = counts[0][1]

        for output, count in counts[1:]:
            if count > best_count:
                best_output = output
                best_count = count

        return ValueNode(best_output)

class SupervisedMeanLeafBuilder(Generic[DataT, InputT], ILeafBuilder[DataT, InputT, float]):
    def __init__(self, output_getter: Callable[[DataT], float]) -> None:
        if output_getter is None:
            raise ValueError('[output_getter] cannot be None!')
        self.OutputGetter = output_getter

    def Build(self, data: Sequence[DataT]) -> INode[InputT, float]:
        if len(data) == 0:
            raise ValueError('Cannot build a mean leaf from empty data!')

        values = [self.OutputGetter(item) for item in data]
        return ValueNode(sum(values) / len(values))

class FunctionSplitPartitioner(Generic[DataT, InputT, BranchT], ISplitPartitioner[DataT, InputT, BranchT]):
    def __init__(
        self,
        function: Callable[
            [Sequence[DataT], ISplit[InputT, BranchT]],
            IInspectableBranchMapping[BranchT, Sequence[DataT]]
        ]
    ) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Partition(
        self,
        data: Sequence[DataT],
        split: ISplit[InputT, BranchT]
    ) -> IInspectableBranchMapping[BranchT, Sequence[DataT]]:
        return self.Function(data, split)

class InputSplitPartitioner(Generic[DataT, InputT, BranchT], ISplitPartitioner[DataT, InputT, BranchT]):
    def __init__(self, input_getter: Callable[[DataT], InputT]) -> None:
        if input_getter is None:
            raise ValueError('[input_getter] cannot be None!')
        self.InputGetter = input_getter

    def Partition(
        self,
        data: Sequence[DataT],
        split: ISplit[InputT, BranchT]
    ) -> IInspectableBranchMapping[BranchT, Sequence[DataT]]:
        groups: list[Tuple[BranchT, list[DataT]]] = []

        for item in data:
            branch = split.Split(self.InputGetter(item))
            found = False

            for current_branch, current_data in groups:
                if current_branch == branch:
                    current_data.append(item)
                    found = True
                    break

            if not found:
                groups.append((branch, [item]))

        return ListBranchMapping(
            (branch, tuple(group))
            for branch, group in groups
        )

class RecursiveGreedyDecisionTreeTrainingStrategy(
    Generic[DataT, InputT, OutputT, BranchT, EvaluateT],
    IDecisionTreeTrainingStrategy[InputT, OutputT]
):
    def __init__(
        self,
        data: Sequence[DataT],
        optimizer: ISplitOptimizer[
            DecisionTreeNodeTrainingState[DataT],
            ISplit[InputT, BranchT],
            IObjective[ISplit[InputT, BranchT], EvaluateT]
        ],
        objective_builder: IObjectiveBuilder[
            DecisionTreeNodeTrainingState[DataT],
            IObjective[ISplit[InputT, BranchT], EvaluateT]
        ],
        partitioner: ISplitPartitioner[DataT, InputT, BranchT],
        leaf_builder: ILeafBuilder[DataT, InputT, OutputT],
        mapping_builder: Optional[
            IBranchMappingBuilder[
                BranchT,
                INode[InputT, OutputT]
            ]
        ] = None,
        stopping_criterion: Optional[
            IStoppingCriterion[DecisionTreeNodeTrainingState[DataT]]
        ] = None
    ) -> None:
        if data is None:
            raise ValueError('[data] cannot be None!')
        if optimizer is None:
            raise ValueError('[optimizer] cannot be None!')
        if objective_builder is None:
            raise ValueError('[objective_builder] cannot be None!')
        if partitioner is None:
            raise ValueError('[partitioner] cannot be None!')
        if leaf_builder is None:
            raise ValueError('[leaf_builder] cannot be None!')

        self.Data = tuple(data)
        self.Optimizer = optimizer
        self.ObjectiveBuilder = objective_builder
        self.Partitioner = partitioner
        self.LeafBuilder = leaf_builder
        self.MappingBuilder = (
            ListBranchMappingBuilder()
            if mapping_builder is None
            else mapping_builder
        )
        self.StoppingCriterion = stopping_criterion

    def Train(self, model: DecisionTree[InputT, OutputT]) -> None:
        if model is None:
            raise ValueError('[model] cannot be None!')
        if len(self.Data) == 0:
            raise ValueError('Cannot train a decision tree with empty data!')

        root_state = DecisionTreeNodeTrainingState(self.Data, 0)
        model.SetRoot(self.__BuildNode(root_state))

    def __BuildNode(
        self,
        state: DecisionTreeNodeTrainingState[DataT]
    ) -> INode[InputT, OutputT]:
        if self.StoppingCriterion is not None and self.StoppingCriterion.ShouldStop(state):
            return self.LeafBuilder.Build(state.Data)

        objective = self.ObjectiveBuilder.Build(state)

        try:
            split = self.Optimizer.Optimize(state, objective)
        except NoSplitCandidateError:
            return self.LeafBuilder.Build(state.Data)

        partitions = tuple(self.Partitioner.Partition(state.Data, split).GetItems())
        partitions = tuple(
            (branch, data)
            for branch, data in partitions
            if len(data) > 0
        )

        # A split that produces fewer than two non-empty branches did not
        # actually divide the local training problem, so recursion must stop.
        if len(partitions) < 2:
            return self.LeafBuilder.Build(state.Data)

        children = []

        for branch, child_data in partitions:
            child_state = DecisionTreeNodeTrainingState(
                tuple(child_data),
                state.Depth + 1
            )
            children.append(
                (branch, self.__BuildNode(child_state))
            )

        mapping = self.MappingBuilder.Build(children)
        distributor = SplitDistributor(split, mapping)
        return DistributorBranchNode(distributor)
