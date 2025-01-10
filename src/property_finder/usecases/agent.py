from abc import ABC
from typing import Any, Dict

from src.property_finder.models import Agent
from src.property_finder.services.agent_service import AgentService
from src.property_finder.usecases import IUseCase


class BaseAgentUseCase(IUseCase, ABC):
    def __init__(self):
        self._service = AgentService()


class CreateAgentUseCase(BaseAgentUseCase):
    def execute(self, name: str, email: str, phone_number: str) -> Agent:
        return self._service.create_agent(name=name, email=email, phone_number=phone_number)


class UpdateAgentUseCase(BaseAgentUseCase):
    def execute(self, pk: int, updates: Dict[str, Any]) -> Agent:
        return self._service.update_agent(pk=pk, updates=updates)


class DeleteAgentUseCase(BaseAgentUseCase):
    def execute(self, pk: int):
        self._service.delete_agent(pk=pk)


class SearchAgentUseCase(BaseAgentUseCase):
    def execute(self, pk: int, filters: Dict[str, Any]) -> Dict[str, Any]:
        return self._service.search_agents(pk=pk, filters=filters)
