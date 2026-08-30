from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TypeVar, Generic, Tuple, TypeVarTuple

__all__ = ["IData", "StructData", "TupleData"]

DataT = TypeVar('DataT')

class IData(ABC, Generic[DataT]):
    @abstractmethod
    def GetData(self) -> DataT:
        pass

@dataclass
class StructData(Generic[DataT], IData[DataT]):
    Data: DataT

    def GetData(self) -> DataT:
        return self.Data

DataTTuple = TypeVarTuple('DataTTuple')

class TupleData(Generic[*DataTTuple], StructData[Tuple[*DataTTuple]]):
    def GetSize(self) -> int:
        return len(self.Data)

    def GetAt(self, idx: int):
        return None if idx < 0 or idx >= self.GetSize() else self.Data[idx]
