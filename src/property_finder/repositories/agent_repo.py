from typing import Any

from django.db.models import QuerySet

from src.property_finder.models import Agent
from src.property_finder.repositories.base_repo import ICRUDRepository


class AgentRepository(ICRUDRepository):
    def all(self) -> QuerySet[Agent]:
        pass

    def filter_by_fields(self, data: dict[str:Any]) -> QuerySet[Agent]:
        pass

    def find_by_id(self, pk: int) -> Any:
        pass

    def create(self, name: str, email: str, phone_number: str) -> Any:
        pass

    def delete(self, pk: int):
        pass

    def update(self, data: [str, Any]) -> Any:
        pass
