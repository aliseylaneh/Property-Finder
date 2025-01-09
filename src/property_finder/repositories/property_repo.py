from typing import Any

from django.db.models import QuerySet

from src.property_finder.models import Property
from src.property_finder.repositories.base_repo import ICRUDRepository


class PropertyRepository(ICRUDRepository):

    def all(self) -> QuerySet[Property]:
        pass

    def filter_by_fields(self, data: dict[str:Any]) -> QuerySet[Property]:
        pass

    def find_by_id(self, pk: int) -> Property:
        pass

    def create(self, name: str, email: str, phone_number: str) -> Property:
        pass

    def delete(self, pk: int):
        pass

    def update(self, data: [str, Any]) -> Property:
        pass
