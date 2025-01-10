from typing import Any, Dict

from src.property_finder.models import Property
from src.property_finder.repositories.django.property_repo import PropertyDjangoRepository
from src.property_finder.repositories.es.property_repo import PropertyElasticSearchRepository


class PropertyService:
    def __init__(self):
        self._django_repository = PropertyDjangoRepository()
        self._elastic_repository = PropertyElasticSearchRepository()

    async def create_property(self, main_type, sub_type, title, description, agent) -> Property:
        property_instance = await self._django_repository.create(
            main_type=main_type,
            sub_type=sub_type,
            title=title,
            description=description,
            agent=agent,
        )
        return property_instance

    async def search_property(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def update_property(self, pk: int, data: Dict[str, Any]) -> Property:
        property_instance = await self._django_repository.update(pk=pk, data=data)
        return property_instance

    async def delete_property(self, pk: int):
        await self._django_repository.delete(pk=pk)
