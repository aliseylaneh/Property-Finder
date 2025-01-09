from typing import Any

from src.property_finder.repositories.es.abstract_repository import IElasticSearchRepository


class PropertyElasticSearchRepository(IElasticSearchRepository):
    async def index(self, *args, **kwargs) -> Any:
        pass

    async def search(self, *args, **kwargs) -> Any:
        pass
