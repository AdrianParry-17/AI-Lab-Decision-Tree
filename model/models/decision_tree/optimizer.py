from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Callable, Iterable, Optional, Sequence, Tuple, List
from ...train.optimizer import IOptimizer
from ...train.objective import IObjective
from .split import (
    ISplit, ValueThresholdSplit,
    AttributeValueSplit, AttributeThresholdSplit
)

__all__ = [
    'NoSplitCandidateError',
    'ISplitOptimizer',
    'ISplitCandidateGenerator', 'FunctionSplitCandidateGenerator',
    'SequenceSplitCandidateGenerator',
    'IEvaluationComparator', 'FunctionEvaluationComparator',
    'MinimizeEvaluationComparator', 'MaximizeEvaluationComparator',
    'BestSplitOptimizer',
    'ScalarThresholdSplitCandidateGenerator',
    'AttributeSplitCandidateGenerator'
]

# --- Generic stuff ---

InputStateT = TypeVar('InputStateT')
InputT = TypeVar('InputT')
BranchT = TypeVar('BranchT')
EvaluateT = TypeVar('EvaluateT')
OutputSplitT = TypeVar('OutputSplitT', bound=ISplit[Any, Any])
ObjectiveT = TypeVar('ObjectiveT', bound=IObjective[Any, Any])
DataT = TypeVar('DataT')
AttributeNameT = TypeVar('AttributeNameT')
AttributeValueT = TypeVar('AttributeValueT')

class NoSplitCandidateError(RuntimeError):
    pass

class ISplitOptimizer(Generic[InputStateT, OutputSplitT, ObjectiveT],
                      IOptimizer[InputStateT, OutputSplitT, ObjectiveT]):
    pass

class ISplitCandidateGenerator(ABC, Generic[InputStateT, OutputSplitT]):
    @abstractmethod
    def Generate(self, state: InputStateT) -> Iterable[OutputSplitT]:
        pass

class IEvaluationComparator(ABC, Generic[EvaluateT]):
    @abstractmethod
    def IsBetter(self, candidate: EvaluateT, current: EvaluateT) -> bool:
        pass

# --- Specific stuff ---

class FunctionSplitCandidateGenerator(Generic[InputStateT, OutputSplitT], ISplitCandidateGenerator[InputStateT, OutputSplitT]):
    def __init__(self, function: Callable[[InputStateT], Iterable[OutputSplitT]]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Generate(self, state: InputStateT) -> Iterable[OutputSplitT]:
        return self.Function(state)

class SequenceSplitCandidateGenerator(Generic[InputStateT, OutputSplitT], ISplitCandidateGenerator[InputStateT, OutputSplitT]):
    def __init__(self, splits: Sequence[OutputSplitT]) -> None:
        if splits is None:
            raise ValueError('[splits] cannot be None!')
        self.Splits = tuple(splits)

    def Generate(self, state: InputStateT) -> Iterable[OutputSplitT]:
        return self.Splits

class FunctionEvaluationComparator(Generic[EvaluateT], IEvaluationComparator[EvaluateT]):
    def __init__(self, function: Callable[[EvaluateT, EvaluateT], bool]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def IsBetter(self, candidate: EvaluateT, current: EvaluateT) -> bool:
        return self.Function(candidate, current)

class MinimizeEvaluationComparator(Generic[EvaluateT], IEvaluationComparator[EvaluateT]):
    def IsBetter(self, candidate: EvaluateT, current: EvaluateT) -> bool:
        return candidate < current

class MaximizeEvaluationComparator(Generic[EvaluateT], IEvaluationComparator[EvaluateT]):
    def IsBetter(self, candidate: EvaluateT, current: EvaluateT) -> bool:
        return candidate > current

class BestSplitOptimizer(Generic[InputStateT, InputT, BranchT, EvaluateT],
                         ISplitOptimizer[InputStateT, ISplit[InputT, BranchT], IObjective[ISplit[InputT, BranchT], EvaluateT]]):
    def __init__(self, generator: ISplitCandidateGenerator[InputStateT, ISplit[InputT, BranchT]],
                 comparator: IEvaluationComparator[EvaluateT]) -> None:
        if generator is None:
            raise ValueError('[generator] cannot be None!')
        if comparator is None:
            raise ValueError('[comparator] cannot be None!')

        self.Generator = generator
        self.Comparator = comparator

    def Optimize(self, state: InputStateT, objective: IObjective[ISplit[InputT, BranchT], EvaluateT]) -> ISplit[InputT, BranchT]:
        best_split: Optional[ISplit[InputT, BranchT]] = None
        best_evaluation: Optional[EvaluateT] = None
        has_evaluation = False

        for split in self.Generator.Generate(state):
            evaluation = objective.Evaluate(split)

            if not has_evaluation or self.Comparator.IsBetter(evaluation, best_evaluation):
                best_split = split
                best_evaluation = evaluation
                has_evaluation = True

        if best_split is None:
            raise NoSplitCandidateError('No split candidate was generated!')

        return best_split

class ScalarThresholdSplitCandidateGenerator(Generic[InputStateT, DataT], ISplitCandidateGenerator[InputStateT, ISplit[float, bool]]):
    def __init__(self, data_getter: Callable[[InputStateT], Sequence[DataT]], input_getter: Callable[[DataT], float]) -> None:
        if data_getter is None:
            raise ValueError('[data_getter] cannot be None!')
        if input_getter is None:
            raise ValueError('[input_getter] cannot be None!')
        self.DataGetter = data_getter
        self.InputGetter = input_getter

    def Generate(self, state: InputStateT) -> Iterable[ISplit[float, bool]]:
        values = sorted(set(self.InputGetter(data) for data in self.DataGetter(state)))

        for i in range(len(values) - 1):
            yield ValueThresholdSplit((values[i] + values[i + 1]) / 2.0)

class AttributeSplitCandidateGenerator(Generic[InputStateT, DataT, AttributeNameT, AttributeValueT],
                                       ISplitCandidateGenerator[InputStateT, ISplit[List[Tuple[AttributeNameT, AttributeValueT]], object]]):
    def __init__(self, data_getter: Callable[[InputStateT], Sequence[DataT]],
                 input_getter: Callable[[DataT], List[Tuple[AttributeNameT, AttributeValueT]]],
                 continuous: Optional[Callable[[AttributeNameT, Sequence[AttributeValueT]], bool]] = None) -> None:
        if data_getter is None:
            raise ValueError('[data_getter] cannot be None!')
        if input_getter is None:
            raise ValueError('[input_getter] cannot be None!')

        self.DataGetter = data_getter
        self.InputGetter = input_getter
        self.Continuous = continuous

    def __IsContinuous(self, name: AttributeNameT, values: Sequence[AttributeValueT]) -> bool:
        if self.Continuous is not None:
            return self.Continuous(name, values)

        return len(values) > 0 and all(
            isinstance(value, (int, float)) and not isinstance(value, bool)
            for value in values
        )

    def Generate(self, state: InputStateT) -> Iterable[ISplit[List[Tuple[AttributeNameT, AttributeValueT]], object]]:
        data = self.DataGetter(state)
        if len(data) == 0:
            return

        names: List[AttributeNameT] = []
        for name, _ in self.InputGetter(data[0]):
            if not any(current == name for current in names):
                names.append(name)

        for name in names:
            values: List[AttributeValueT] = []

            for item in data:
                found = False
                for current_name, value in self.InputGetter(item):
                    if current_name == name:
                        values.append(value)
                        found = True
                        break
                if not found:
                    break

            if len(values) != len(data):
                continue

            if self.__IsContinuous(name, values):
                numeric_values = sorted(set(float(value) for value in values))
                for i in range(len(numeric_values) - 1):
                    threshold = (numeric_values[i] + numeric_values[i + 1]) / 2.0
                    yield AttributeThresholdSplit(name, threshold)
            else:
                yield AttributeValueSplit(name)
