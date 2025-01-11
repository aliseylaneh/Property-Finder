from typing import Any

from elasticsearch import NotFoundError

from property_finder.es.documents.agent import AgentDocument
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories import AbstractRepository


class AgentElasticSearchRepository(AbstractRepository):

    def index(self, pk: int, name: str, email: str, phone_number: str):
        pass

    def search(self, *args, **kwargs) -> Any:
        pass

    def update(self, *args, **kwargs):
        pass

    def delete(self, pk: str):
        try:
            agent_instance = AgentDocument.get(id=pk)
            agent_instance.delete()
        except NotFoundError:
            raise AgentNotFound()
