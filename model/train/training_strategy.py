from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any
from ..model import IModel

__all__ = ['ITrainingStrategy']

# --- Generic stuff ---

ModelT = TypeVar('ModelT', bound=IModel[Any, Any])

class ITrainingStrategy(ABC, Generic[ModelT]):
    @abstractmethod
    def Train(self, model: ModelT) -> None:
        pass
