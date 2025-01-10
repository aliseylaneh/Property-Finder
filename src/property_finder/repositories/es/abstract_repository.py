from abc import abstractmethod
from typing import Any

from src.property_finder.repositories import AbstractRepository


class IElasticSearchRepository(AbstractRepository):
    @abstractmethod
    def index(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def search(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
