from typing import Any

from elasticsearch import NotFoundError

from src.property_finder.models.es.agent import AgentDocument
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories.es.abstract_repository import IElasticSearchRepository


class AgentElasticSearchRepository(IElasticSearchRepository):

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

    def index(self, pk: int, name: str, email: str, phone_number: str):
        doc = AgentDocument(
            meta={'id': pk},
            name=name,
            email=email,
            phone_number=phone_number
        )
        doc.save()
