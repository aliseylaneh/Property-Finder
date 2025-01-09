from src.property_finder.models import Agent
from src.property_finder.repositories.django.agent_repo import AgentRepository


class AgentService:

    def __init__(self):
        self._django_repository = AgentRepository()
        self._elastic_repository = None

    async def create_agent(self, name: str, email: str, phone_number: str) -> Agent:
        instance = await self._django_repository.create(name=name, email=email, phone_number=phone_number)
        # TODO insert data into elasticsearch
        return instance

    async def delete_agent(self, pk: int):
        await self._django_repository.delete(pk=pk)

    async def search_agents(self):
        pass
