from typing import Any

from elasticsearch import NotFoundError

from src.property_finder.models.es.agent import AgentDocument
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories.es.abstract_repository import IElasticSearchRepository


class AgentElasticSearchRepository(IElasticSearchRepository):

    async def delete(self, pk: str):
        try:
            agent_instance = await AgentDocument.get(id=pk)
            await agent_instance.delete()
        except NotFoundError:
            raise AgentNotFound()

    async def index(self, pk: int, name: str, email: str, phone_number: str):
        doc = AgentDocument(
            meta={'id': pk},
            name=name,
            email=email,
            phone_number=phone_number
        )
        await doc.save()

    async def search(self, *args, **kwargs) -> Any:
        AgentDocument.search()
