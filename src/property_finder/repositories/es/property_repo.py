from typing import Any

from src.property_finder.models.es.property import PropertyDocument
from src.property_finder.repositories.es.abstract_repository import IElasticSearchRepository


class PropertyElasticSearchRepository(IElasticSearchRepository):

    async def index(self,
                    pk: int,
                    main_type_name: str,
                    sub_type_name: str,
                    title: str,
                    description: str,
                    agent_name: str) -> PropertyDocument:
        doc = await PropertyDocument(
            meta={'id': pk},
            main_type=main_type_name,
            sub_type=sub_type_name,
            title=title,
            description=description,
            agent_name=agent_name,
        )
        doc = await doc.save()
        return doc

    async def search(self, main_type: str, sub_type: str, title: str) -> Any:
        PropertyDocument.search()
