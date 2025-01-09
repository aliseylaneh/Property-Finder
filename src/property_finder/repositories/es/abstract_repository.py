from abc import abstractmethod
from typing import Any

from src.property_finder.repositories import AbstractRepository


class IElasticSearchRepository(AbstractRepository):
    @abstractmethod
    async def index(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def search(self, *args, **kwargs) -> Any:
        raise NotImplementedError
