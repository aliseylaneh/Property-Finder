from typing import Any, Dict

from src.property_finder.models.documents.property import PropertyDocument
from src.property_finder.repositories import AbstractRepository


class PropertyElasticSearchRepository(AbstractRepository):

    def index(self, pk: int, main_type_name: str,
              sub_type_name: str, title: str, description: str,
              agent_name: str) -> PropertyDocument:
        pass

    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def delete(self, pk: int) -> None:
        pass

    def update(self, pk: str, updates: Dict[str, Any]) -> PropertyDocument:
        pass
