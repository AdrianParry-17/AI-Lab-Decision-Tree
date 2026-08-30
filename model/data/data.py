from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TypeVar, Generic, Tuple, TypeVarTuple

__all__ = ["IData", "ValueData", "TupleData"]

# --- Generic stuff ---

DataT = TypeVar('DataT')

class IData(ABC, Generic[DataT]):
    """Basically, base class of all data."""
    @abstractmethod
    def GetData(self) -> DataT:
        pass

# --- Specific stuff ---

@dataclass
class ValueData(Generic[DataT], IData[DataT]):
    """A data that only contain the value explicitly as variable."""
    Data: DataT

    def GetData(self) -> DataT:
        return self.Data

DataTTuple = TypeVarTuple('DataTTuple')

class TupleData(Generic[*DataTTuple], ValueData[Tuple[*DataTTuple]]):
    def GetSize(self) -> int:
        return len(self.Data)

    def GetAt(self, idx: int):
        return None if idx < 0 or idx >= self.GetSize() else self.Data[idx]
