from abc import ABC, abstractmethod
from math import log2
from typing import TypeVar, Generic, Callable, Sequence, Tuple, List
from ...train.objective import IObjective
from .split import ISplit

__all__ = [
    'IObjectiveBuilder', 'FunctionObjectiveBuilder',
    'ISplitObjective', 'SupervisedSplitObjective',
    'Entropy', 'Gini', 'ClassificationError', 'SSE',
    'WeightedImpuritySplitObjective', 'SummedImpuritySplitObjective'
]

# --- Generic stuff ---

StateT = TypeVar('StateT')
ObjectiveT = TypeVar('ObjectiveT')
DataT = TypeVar('DataT')
InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
BranchT = TypeVar('BranchT')
EvaluateT = TypeVar('EvaluateT')

class IObjectiveBuilder(ABC, Generic[StateT, ObjectiveT]):
    @abstractmethod
    def Build(self, state: StateT) -> ObjectiveT:
        pass

class ISplitObjective(Generic[InputT, BranchT, EvaluateT], IObjective[ISplit[InputT, BranchT], EvaluateT]):
    pass

# --- Specific stuff ---

class FunctionObjectiveBuilder(Generic[StateT, ObjectiveT], IObjectiveBuilder[StateT, ObjectiveT]):
    def __init__(self, function: Callable[[StateT], ObjectiveT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Build(self, state: StateT) -> ObjectiveT:
        return self.Function(state)

class SupervisedSplitObjective(Generic[DataT, InputT, OutputT, BranchT], ISplitObjective[InputT, BranchT, float]):
    def __init__(self, data: Sequence[DataT], extractor: Callable[[DataT], Tuple[InputT, OutputT]]) -> None:
        if data is None:
            raise ValueError('[data] cannot be None!')
        if extractor is None:
            raise ValueError('[extractor] cannot be None!')
        self.Data = tuple(data)
        self.Extractor = extractor

    def _PartitionOutputs(self, split: ISplit[InputT, BranchT]) -> List[Tuple[BranchT, List[OutputT]]]:
        groups: List[Tuple[BranchT, List[OutputT]]] = []

        for data in self.Data:
            x, y = self.Extractor(data)
            branch = split.Split(x)

            found = False
            for current_branch, outputs in groups:
                if current_branch == branch:
                    outputs.append(y)
                    found = True
                    break

            if not found:
                groups.append((branch, [y]))

        return groups

class WeightedImpuritySplitObjective(Generic[DataT, InputT, OutputT, BranchT],
                                     SupervisedSplitObjective[DataT, InputT, OutputT, BranchT]):
    def __init__(self, data: Sequence[DataT],
                 extractor: Callable[[DataT], Tuple[InputT, OutputT]],
                 impurity: Callable[[Sequence[OutputT]], float]) -> None:
        if impurity is None:
            raise ValueError('[impurity] cannot be None!')
        super().__init__(data, extractor)
        self.Impurity = impurity

    def Evaluate(self, split: ISplit[InputT, BranchT]) -> float:
        if len(self.Data) == 0:
            return 0.0

        score = 0.0
        total = len(self.Data)

        for _, outputs in self._PartitionOutputs(split):
            score += (len(outputs) / total) * self.Impurity(outputs)

        return score

class SummedImpuritySplitObjective(Generic[DataT, InputT, OutputT, BranchT],
                                   SupervisedSplitObjective[DataT, InputT, OutputT, BranchT]):
    def __init__(self, data: Sequence[DataT],
                 extractor: Callable[[DataT], Tuple[InputT, OutputT]],
                 impurity: Callable[[Sequence[OutputT]], float]) -> None:
        if impurity is None:
            raise ValueError('[impurity] cannot be None!')
        super().__init__(data, extractor)
        self.Impurity = impurity

    def Evaluate(self, split: ISplit[InputT, BranchT]) -> float:
        return sum(self.Impurity(outputs) for _, outputs in self._PartitionOutputs(split))

# --- Common objective functions ---

def _Counts(values: Sequence[OutputT]) -> List[Tuple[OutputT, int]]:
    counts: List[Tuple[OutputT, int]] = []

    for value in values:
        found = False
        for i, (current, count) in enumerate(counts):
            if current == value:
                counts[i] = (current, count + 1)
                found = True
                break
        if not found:
            counts.append((value, 1))

    return counts

def Entropy(values: Sequence[OutputT]) -> float:
    if len(values) == 0:
        return 0.0

    n = len(values)
    result = 0.0

    for _, count in _Counts(values):
        p = count / n
        result -= p * log2(p)

    return result

def Gini(values: Sequence[OutputT]) -> float:
    if len(values) == 0:
        return 0.0

    n = len(values)
    return 1.0 - sum(
        (count / n) ** 2
        for _, count in _Counts(values)
    )

def ClassificationError(values: Sequence[OutputT]) -> float:
    if len(values) == 0:
        return 0.0

    n = len(values)
    best = max(count for _, count in _Counts(values))
    return 1.0 - (best / n)

def SSE(values: Sequence[float]) -> float:
    if len(values) == 0:
        return 0.0

    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values)
