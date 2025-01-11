from typing import Any, Dict, List

from elasticsearch import NotFoundError
from elasticsearch_dsl import Q

from src.property_finder.es.documents.property import PropertyDocument
from src.property_finder.models.exceptions.property import PropertyNotFound


class PropertyElasticSearchRepository:

    def index(self, pk: int, main_type: Dict[str, Any], sub_type: Dict[str, Any], title: str, description: str, agent: Dict[str, Any]) -> PropertyDocument:
        """
        Index a new property document in Elasticsearch.
        :param pk: Property Document ID
        :param main_type: Main Type
        :param sub_type: Sub Type
        :param title: Title
        :param description: Description
        :param agent: Agent Name
        :return: Property Document
        """
        property_document = PropertyDocument(
            meta={'id': pk},
            title=title,
            description=description,
            main_type=main_type,
            sub_type=sub_type,
            agent=agent
        )
        property_document.save()
        return property_document

    def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Perform a search query on the Property document.
        :param query: The query to search for
        :**kwargs: Arbitrary keyword arguments which should include size and page for pagination
        :return: Dict[str, Any]: Search results
        """
        search = PropertyDocument.search().query(
            "function_score",
            query=Q("bool", should=[
                Q("match", title={"query": query, "boost": 5}),
                Q("match", sub_type__title={"query": query, "boost": 3}),
                Q("match", main_type__title={"query": query, "boost": 2}),
            ]),
            functions=[
                {"script_score": {
                    "script": {
                        "source": """
                                        double score = 0;
                                        if (doc['title.keyword'].size() != 0 && doc['title.keyword'].value == params.query) score += 10;
                                        if (doc['sub_type.title.keyword'].size() != 0 && doc['sub_type.title.keyword'].value == params.query) score += 5;
                                        if (doc['main_type.title.keyword'].size() != 0 && doc['main_type.title.keyword'].value == params.query) score += 3;
                                        return score;
                                    """,
                        "params": {
                            "query": query
                        }
                    }
                }
                }
            ],
            boost_mode="sum"
        ).extra(size=kwargs.get('size', 10), from_=(kwargs.get('page', 1) - 1) * kwargs.get('size', 10))
        results = search.execute()
        query_results = [{"id": hit.meta.id, "score": hit.meta.score, "title": hit.title, "main_type": hit.main_type.title,
                          "sub_type": hit.sub_type.title, "agent": hit.agent.name} for hit in results]
        return query_results

    def delete(self, pk: int) -> None:
        """
        Delete a property document from Elasticsearch by its ID.
        :param pk: Primary key of the property
        """
        try:
            property_document = PropertyDocument.get(id=str(pk))
            property_document.delete()
        except NotFoundError:
            raise PropertyNotFound()

    def find_by_id(self, pk: int) -> PropertyDocument:
        """
        Find a property document by its ID.
        :param pk: Primary key of the property
        """
        try:
            property_document = PropertyDocument.get(id=str(pk))
            return property_document
        except NotFoundError:
            raise PropertyNotFound()

    def update(self, pk: int, updates: Dict[str, Any]) -> PropertyDocument:
        """
        Update an existing property document in Elasticsearch.
        :param pk: Primary key of the property
        :param updates: Dictionary of properties to update
        """
        property_document = self.find_by_id(pk=pk)
        for field, value in updates.items():
            setattr(property_document, field, value)
        property_document.save()
        return property_document
