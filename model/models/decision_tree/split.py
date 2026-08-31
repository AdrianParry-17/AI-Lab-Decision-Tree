from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, List, Tuple

__all__ = [
    'ISplit', 'FunctionSplit', 'PredicateSplit',
    'ValueThresholdSplit', 'AttributeValueSplit', 'AttributePredicateSplit',
    'AttributeThresholdSplit'
]

# --- Generic stuff ---

InputT = TypeVar('InputT')
BranchT = TypeVar('BranchT')
AttributeNameT = TypeVar('AttributeNameT')
AttributeValueT = TypeVar('AttributeValueT')

class ISplit(ABC, Generic[InputT, BranchT]):
    @abstractmethod
    def Split(self, x: InputT) -> BranchT:
        pass

# --- Specific stuff ---

class FunctionSplit(Generic[InputT, BranchT], ISplit[InputT, BranchT]):
    def __init__(self, function: Callable[[InputT], BranchT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function: Callable[[InputT], BranchT] = function

    def Split(self, x: InputT) -> BranchT:
        return self.Function(x)

class PredicateSplit(Generic[InputT], FunctionSplit[InputT, bool]):
    pass

class ValueThresholdSplit(Generic[InputT], ISplit[InputT, bool]):
    def __init__(self, threshold: InputT) -> None:
        self.Threshold = threshold

    def Split(self, x: InputT) -> bool:
        return x <= self.Threshold

class AttributeValueSplit(Generic[AttributeNameT, AttributeValueT],
                          ISplit[List[Tuple[AttributeNameT, AttributeValueT]], AttributeValueT]):
    def __init__(self, attribute_name: AttributeNameT) -> None:
        self.AttributeName = attribute_name

    def Split(self, x: List[Tuple[AttributeNameT, AttributeValueT]]) -> AttributeValueT:
        for name, value in x:
            if name == self.AttributeName:
                return value
        raise KeyError(f'Attribute {self.AttributeName!r} does not exist!')

class AttributePredicateSplit(Generic[AttributeNameT, AttributeValueT, BranchT],
                              ISplit[List[Tuple[AttributeNameT, AttributeValueT]], BranchT]):
    def __init__(self, attribute_name: AttributeNameT,
                 predicate: Callable[[AttributeValueT], BranchT]) -> None:
        if predicate is None:
            raise ValueError('[predicate] cannot be None!')
        self.AttributeName = attribute_name
        self.Predicate = predicate

    def Split(self, x: List[Tuple[AttributeNameT, AttributeValueT]]) -> BranchT:
        for name, value in x:
            if name == self.AttributeName:
                return self.Predicate(value)
        raise KeyError(f'Attribute {self.AttributeName!r} does not exist!')

class AttributeThresholdSplit(Generic[AttributeNameT, AttributeValueT],
                              AttributePredicateSplit[AttributeNameT, AttributeValueT, bool]):
    def __init__(self, attribute_name: AttributeNameT, threshold: AttributeValueT) -> None:
        self.Threshold = threshold
        super().__init__(attribute_name, lambda value: value <= threshold)
