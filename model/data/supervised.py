from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Tuple, Any, Callable
from .data import IData

__all__ = ['ISupervisedData']

# --- Abstracting stuff here ---

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')

class ISupervisedData(ABC, Generic[InputT, OutputT]):
    @abstractmethod
    def GetInput(self) -> InputT:
        pass

    @abstractmethod
    def GetOutput(self) -> OutputT:
        pass

DataT = TypeVar('DataT', bound=IData[Any])
SupervisedDataT = TypeVar('SupervisedDataT', bound=ISupervisedData[Any, Any])

class ISupervisedDataExtractor(ABC, Generic[InputT, OutputT, DataT]):
    @abstractmethod
    def Extract(self, data: DataT) -> Tuple[InputT, OutputT]:
        pass

class ISupervisedDataBuilder(ABC, Generic[InputT, OutputT, SupervisedDataT]):
    @abstractmethod
    def Build(self, data: Tuple[InputT, OutputT]) -> SupervisedDataT:
        pass

class ISupervisedDataParser(ABC, Generic[DataT, SupervisedDataT]):
    @abstractmethod
    def Parse(self, data: DataT) -> SupervisedDataT:
        pass

# --- The specific stuff here ---

class ExtractBuildSuperviseDataParser(Generic[InputT, OutputT, DataT, SupervisedDataT], ISupervisedDataParser[DataT, SupervisedDataT]):
    def __init__(self, extractor: ISupervisedDataExtractor[InputT, OutputT, DataT],
                 builder: ISupervisedDataBuilder[InputT, OutputT, SupervisedDataT]) -> None:
        if extractor is None:
            raise ValueError("[extractor] cannot be None!")
        if builder is None:
            raise ValueError("[builder] cannot be None!")

        self.Extractor: ISupervisedDataExtractor[InputT, OutputT, DataT] = extractor
        self.Builder: ISupervisedDataBuilder[InputT, OutputT, SupervisedDataT] = builder

    def Parse(self, data: DataT) -> SupervisedDataT:
        return self.Builder.Build(self.Extractor.Extract(data))

class FunctionSuperviseDataExtractor(Generic[InputT, OutputT, DataT], ISupervisedDataExtractor[InputT, OutputT, DataT]):
    def __init__(self, function: Callable[[DataT], Tuple[InputT, OutputT]]):
        if function is None:
            raise ValueError("[function] cannot be None!")
        self.Function: Callable[[DataT], Tuple[InputT, OutputT]] = function

    def Extract(self, data: DataT) -> Tuple[InputT, OutputT]:
        return self.Function(data)

class FunctionSuperviseDataBuilder(Generic[InputT, OutputT, SupervisedDataT], ISupervisedDataBuilder[InputT, OutputT, SupervisedDataT]):
    def __init__(self, function: Callable[[Tuple[InputT, OutputT]], SupervisedDataT]):
        if function is None:
            raise ValueError("[function] cannot be None!")
        self.Function: Callable[[Tuple[InputT, OutputT]], SupervisedDataT] = function

    def Build(self, data: Tuple[InputT, OutputT]) -> SupervisedDataT:
        return self.Function(data)

class FunctionSuperviseDataParser(Generic[DataT, SupervisedDataT], ISupervisedDataParser[DataT, SupervisedDataT]):
    def __init__(self, function: Callable[[DataT], SupervisedDataT]):
        if function is None:
            raise ValueError("[function] cannot be None!")
        self.Function: Callable[[DataT], SupervisedDataT] = function

    def Parse(self, data: DataT) -> SupervisedDataT:
        return self.Function(data)



@dataclass
class StructSupervisedData(Generic[InputT, OutputT], ISupervisedData[InputT, OutputT]):
    Input: InputT
    Output: OutputT

    def GetInput(self) -> InputT:
        return self.Input

    def GetOutput(self) -> OutputT:
        return self.Output
