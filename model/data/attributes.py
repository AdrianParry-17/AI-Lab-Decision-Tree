from abc import abstractmethod
from typing import Generic, TypeVar, List, Tuple, Optional
from .data import IData
from .supervised import ISupervisedData

__all__ = [
    'IAttributeData', 'IAttributeSupervisedData',
    'RemoveAtAttributeData', 'AttributeAtConvertedSupervisedData'
]

# --- Generic stuff ---

AttributeNameT = TypeVar('AttributeNameT', default=str)
AttributeValueT = TypeVar('AttributeValueT', default=object)

class IAttributeData(Generic[AttributeNameT, AttributeValueT], IData[List[Tuple[AttributeNameT, AttributeValueT]]]):
    @abstractmethod
    def GetSize(self) -> int:
        pass

    @abstractmethod
    def GetNameAt(self, idx: int) -> AttributeNameT:
        pass

    @abstractmethod
    def GetValueAt(self, idx: int) -> AttributeValueT:
        pass

    def GetData(self) -> List[Tuple[AttributeNameT, AttributeValueT]]:
        return [(self.GetNameAt(i), self.GetValueAt(i)) for i in range(self.GetSize())]

    def FindName(self, name: AttributeNameT) -> int:
        return next((i for i in range(self.GetSize()) if name == self.GetNameAt(i)), -1)

    def GetValueFromName(self, name: AttributeNameT) -> Optional[AttributeValueT]:
        return next((self.GetValueAt(i) for i in range(self.GetSize()) if name == self.GetNameAt(i)), None)

    def RemoveAt(self, idx: int) -> 'RemoveAtAttributeData[AttributeNameT, AttributeValueT]':
        return RemoveAtAttributeData(self, idx)

    def ToSupervisedWithOutputAt(self, idx: int) -> 'AttributeAtConvertedSupervisedData[AttributeNameT, AttributeValueT]':
        return AttributeAtConvertedSupervisedData(self, idx)

OutputT = TypeVar('OutputT', default=object)

class IAttributeSupervisedData(
    Generic[AttributeNameT, AttributeValueT, OutputT],
    ISupervisedData[List[Tuple[AttributeNameT, AttributeValueT]], OutputT]
):
    @abstractmethod
    def GetInputSize(self) -> int:
        pass

    @abstractmethod
    def GetInputNameAt(self, idx: int) -> AttributeNameT:
        pass

    @abstractmethod
    def GetInputValueAt(self, idx: int) -> AttributeValueT:
        pass

    def GetInput(self) -> List[Tuple[AttributeNameT, AttributeValueT]]:
        return [(self.GetInputNameAt(i), self.GetInputValueAt(i)) for i in range(self.GetInputSize())]

    def FindInputName(self, name: AttributeNameT) -> int:
        return next((i for i in range(self.GetInputSize()) if name == self.GetInputNameAt(i)), -1)

    def GetInputValueFromName(self, name: AttributeNameT) -> Optional[AttributeValueT]:
        return next((self.GetInputValueAt(i) for i in range(self.GetInputSize()) if name == self.GetInputNameAt(i)), None)

# --- Specific stuff ---

class RemoveAtAttributeData(Generic[AttributeNameT, AttributeValueT], IAttributeData[AttributeNameT, AttributeValueT]):
    def __init__(self, data: IAttributeData[AttributeNameT, AttributeValueT], idx: int) -> None:
        if data is None:
            raise ValueError('[data] cannot be None!')
        self.__data = data
        self.__idx = idx

    def __get_removed_idx(self) -> Optional[int]:
        n = self.__data.GetSize()
        idx = self.__idx + n if self.__idx < 0 else self.__idx
        return idx if 0 <= idx < n else None

    def __get_actual_idx(self, idx: int) -> int:
        n = self.GetSize()
        idx = idx + n if idx < 0 else idx

        if idx < 0 or idx >= n:
            raise IndexError('attribute index out of range')

        removed_idx = self.__get_removed_idx()
        return idx if removed_idx is None or idx < removed_idx else idx + 1

    def GetSize(self) -> int:
        return self.__data.GetSize() - (1 if self.__get_removed_idx() is not None else 0)

    def GetNameAt(self, idx: int) -> AttributeNameT:
        return self.__data.GetNameAt(self.__get_actual_idx(idx))

    def GetValueAt(self, idx: int) -> AttributeValueT:
        return self.__data.GetValueAt(self.__get_actual_idx(idx))

# Bound check on the selected output is intentionally delegated to the underlying data.
class AttributeAtConvertedSupervisedData(
    Generic[AttributeNameT, AttributeValueT],
    IAttributeSupervisedData[AttributeNameT, AttributeValueT, AttributeValueT]
):
    def __init__(self, data: IAttributeData[AttributeNameT, AttributeValueT], idx: int) -> None:
        if data is None:
            raise ValueError('[data] cannot be None!')
        self.__data = data
        self.__inputs = self.__data.RemoveAt(idx)
        self.__idx = idx

    def GetInputSize(self) -> int:
        return self.__inputs.GetSize()

    def GetInputNameAt(self, idx: int) -> AttributeNameT:
        return self.__inputs.GetNameAt(idx)

    def GetInputValueAt(self, idx: int) -> AttributeValueT:
        return self.__inputs.GetValueAt(idx)

    def GetOutput(self) -> AttributeValueT:
        return self.__data.GetValueAt(self.__idx)
