from typing import Any, Dict

from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from src.property_finder.models.es.property import PropertyDocument
from src.property_finder.repositories.es.abstract_repository import IElasticSearchRepository


class PropertyElasticSearchRepository(IElasticSearchRepository):

    def __init__(self, index_name: str = "properties"):
        # Connect to the Elasticsearch cluster
        self.client = connections.create_connection()
        self.index_name = index_name

    async def index(self,
                    pk: int,
                    main_type_name: str,
                    sub_type_name: str,
                    title: str,
                    description: str,
                    agent_name: str) -> PropertyDocument:
        """
        Index a new property document into Elasticsearch.
        """
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
        await property_doc.save()

        return property_doc

    async def search(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for properties based on provided filters.
        """
        # Create a search object
        s = Search(using=self.client, index=self.index_name)

        # Apply filters based on `data`
        for field, value in data.items():
            s = s.filter("term", **{field: value})

        # Execute the search asynchronously
        response = await s.execute()

        # Return the search results
        return {
            "hits": [hit.to_dict() for hit in response],
            "total": response.hits.total.value
        }

    async def delete(self, pk: int) -> None:
        """
        Delete a property document by its primary key (ID).
        """
        property_doc = await PropertyDocument.get(id=str(pk))
        await property_doc.delete()

    async def update(self, pk: str, updates: Dict[str, Any]) -> PropertyDocument:
        """
        Update a property document.
        """
        property_doc = await PropertyDocument.get(id=pk)
        for field, value in updates.items():
            setattr(property_doc, field, value)

        # Save the updated document
        await property_doc.save()

        return property_doc
