from typing import Any, Dict

from src.property_finder.repositories.django.property_repo import PropertyDjangoRepository
from src.property_finder.repositories.es.property_repo import PropertyElasticSearchRepository


class PropertyService:
    def __init__(self):
        self._django_repository = PropertyDjangoRepository()
        self._elastic_repository = PropertyElasticSearchRepository()

    async def create_property(self, main_type, sub_type, title, description, agent):
        # Create property in Django
        property_instance = await self._django_repository.create(
            main_type=main_type,
            sub_type=sub_type,
            title=title,
            description=description,
            agent=agent,
        )

        # Index property in Elasticsearch
        await self._elastic_repository.index(
            pk=property_instance.id,
            main_type_name=property_instance.main_type.title,
            sub_type_name=property_instance.sub_type.title,
            title=property_instance.title,
            description=property_instance.description,
            agent_name=property_instance.agent.name,
        )

        return property_instance

    async def search_property(self, data: Dict[str, Any]):
        pass

    async def update_property(self, data: Dict[str, Any]):
        pass
