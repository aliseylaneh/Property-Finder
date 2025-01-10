from src.property_finder.models import Agent
from src.property_finder.repositories.django.agent_repo import AgentDjangoRepository
from src.property_finder.repositories.es.agent_repo import AgentElasticSearchRepository


class AgentService:
    def __init__(self):
        self._django_repository = AgentDjangoRepository()
        self._elastic_repository = AgentElasticSearchRepository()

    async def create_agent(self, name: str, email: str, phone_number: str) -> Agent:
        # Save to PostgresSQL
        instance = await self._django_repository.create(name=name, email=email, phone_number=phone_number)

        # Index in Elasticsearch
        await self._elastic_repository.index(
            pk=instance.id,
            name=instance.name,
            email=instance.email,
            phone_number=instance.phone_number
        )
        return instance
