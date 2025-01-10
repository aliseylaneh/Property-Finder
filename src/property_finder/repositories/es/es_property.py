from typing import Any, Dict

from src.property_finder.models.documents.property import PropertyDocument
from src.property_finder.repositories import AbstractRepository


class PropertyElasticSearchRepository(AbstractRepository):

    def index(self, pk: int,
              main_type_name: str,
              sub_type_name: str,
              title: str,
              description: str,
              agent_name: str) -> PropertyDocument:
        # Create a new document instance
        property_doc = PropertyDocument(
            meta={'id': pk},
            main_type=main_type_name,
            sub_type=sub_type_name,
            title=title,
            description=description,
            agent_name=agent_name
        )
        # Save the document
        property_doc.save()

        return property_doc

    def search(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def delete(self, pk: int) -> None:
        pass

    def update(self, pk: str, updates: Dict[str, Any]) -> PropertyDocument:
        pass
