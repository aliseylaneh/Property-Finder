from typing import Any, Dict

from src.property_finder.models import Agent
from src.property_finder.repositories.django.agent import AgentDjangoRepository
from src.property_finder.repositories.es.es_agent import AgentElasticSearchRepository


class AgentService:
    def __init__(self):
        self._django_repository = AgentDjangoRepository()
        self._elastic_repository = AgentElasticSearchRepository()

    def find_agent(self, pk: int):
        return self._django_repository.find_by_id(pk=pk)

    def create_agent(self, name: str, email: str, phone_number: str) -> Agent:
        instance = self._django_repository.create(name=name, email=email, phone_number=phone_number)
        return instance

    def update_agent(self, pk: int, updates: Dict[str, Any]) -> Agent:
        return self._django_repository.update(pk=pk, updates=updates)

    def delete_agent(self, pk: int):
        self._django_repository.delete(pk=pk)

    def search_agents(self, pk: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        return self._elastic_repository.search(pk=pk, filters=filters)
