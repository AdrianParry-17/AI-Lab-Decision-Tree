from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Iterable, Mapping, Tuple

__all__ = [
    'IBranchMapping', 'IInspectableBranchMapping',
    'FunctionBranchMapping', 'ListBranchMapping', 'DictionaryBranchMapping',
    'IBranchMappingBuilder', 'FunctionBranchMappingBuilder',
    'ListBranchMappingBuilder'
]

# --- Generic stuff ---

BranchT = TypeVar('BranchT')
ValueT = TypeVar('ValueT')

class IBranchMapping(ABC, Generic[BranchT, ValueT]):
    @abstractmethod
    def Map(self, branch: BranchT) -> ValueT:
        pass

class IInspectableBranchMapping(Generic[BranchT, ValueT], IBranchMapping[BranchT, ValueT]):
    @abstractmethod
    def GetItems(self) -> Iterable[Tuple[BranchT, ValueT]]:
        pass

    def GetBranches(self) -> Iterable[BranchT]:
        return (branch for branch, _ in self.GetItems())

    def GetValues(self) -> Iterable[ValueT]:
        return (value for _, value in self.GetItems())

class IBranchMappingBuilder(ABC, Generic[BranchT, ValueT]):
    @abstractmethod
    def Build(self, items: Iterable[Tuple[BranchT, ValueT]]) -> IBranchMapping[BranchT, ValueT]:
        pass

# --- Specific stuff ---

class FunctionBranchMapping(Generic[BranchT, ValueT], IBranchMapping[BranchT, ValueT]):
    def __init__(self, function: Callable[[BranchT], ValueT]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function: Callable[[BranchT], ValueT] = function

    def Map(self, branch: BranchT) -> ValueT:
        return self.Function(branch)

class ListBranchMapping(Generic[BranchT, ValueT], IInspectableBranchMapping[BranchT, ValueT]):
    def __init__(self, items: Iterable[Tuple[BranchT, ValueT]]) -> None:
        if items is None:
            raise ValueError('[items] cannot be None!')

        self.__items = list(items)

        for i in range(len(self.__items)):
            for j in range(i + 1, len(self.__items)):
                if self.__items[i][0] == self.__items[j][0]:
                    raise ValueError(f'Duplicate branch: {self.__items[i][0]!r}')

    def Map(self, branch: BranchT) -> ValueT:
        for current_branch, value in self.__items:
            if current_branch == branch:
                return value
        raise KeyError(f'No mapping exists for branch {branch!r}')

    def GetItems(self) -> Iterable[Tuple[BranchT, ValueT]]:
        return tuple(self.__items)

class DictionaryBranchMapping(Generic[BranchT, ValueT], IInspectableBranchMapping[BranchT, ValueT]):
    def __init__(self, mapping: Mapping[BranchT, ValueT]) -> None:
        if mapping is None:
            raise ValueError('[mapping] cannot be None!')
        self.__mapping = dict(mapping)

    def Map(self, branch: BranchT) -> ValueT:
        return self.__mapping[branch]

    def GetItems(self) -> Iterable[Tuple[BranchT, ValueT]]:
        return tuple(self.__mapping.items())

class FunctionBranchMappingBuilder(Generic[BranchT, ValueT], IBranchMappingBuilder[BranchT, ValueT]):
    def __init__(self, function: Callable[[Iterable[Tuple[BranchT, ValueT]]], IBranchMapping[BranchT, ValueT]]) -> None:
        if function is None:
            raise ValueError('[function] cannot be None!')
        self.Function = function

    def Build(self, items: Iterable[Tuple[BranchT, ValueT]]) -> IBranchMapping[BranchT, ValueT]:
        return self.Function(items)

class ListBranchMappingBuilder(Generic[BranchT, ValueT], IBranchMappingBuilder[BranchT, ValueT]):
    def Build(self, items: Iterable[Tuple[BranchT, ValueT]]) -> IBranchMapping[BranchT, ValueT]:
        return ListBranchMapping(items)
