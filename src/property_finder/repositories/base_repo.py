from abc import abstractmethod
from typing import Any

from src.property_finder.repositories import AbstractRepository


class ICRUDRepository(AbstractRepository):
    @abstractmethod
    def all(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def filter_by_fields(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def create(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs) -> Any:
        raise NotImplementedError
