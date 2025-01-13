from typing import Any, Dict, List, Tuple

from elasticsearch import NotFoundError
from elasticsearch_dsl.query import Q

from src.property_finder.repositories.es.services import document_update as DocumentUpdateService
from src.property_finder.es.documents.agent import AgentDocument
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories import AbstractRepository


class AgentElasticSearchRepository(AbstractRepository):

    def index(self, pk: int, name: str, email: str, phone_number: str) -> AgentDocument:
        """
        Index a new Agent document in Elasticsearch.
        :param pk: Agent ID
        :param name: Agent name
        :param email: Agent email
        :param phone_number: Agent phone number
        """
        agent_document = AgentDocument(
            meta={'id': pk},
            name=name,
            email=email,
            phone_number=phone_number,
        )
        agent_document.save()
        return agent_document

    def search(self, query: str, size: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        Perform a search query on the Agent document.
        :param query: The query to search for
        :param size: Number of results to return
        :param page: Page number
        :return: List[Dict[str, Any]]: Search results
        """
        search = AgentDocument.search().query(
            "function_score",
            # multi_match helps us to make sure that partial matching in done on name field.
            query=Q("multi_match", query=query, fields=["name^5"]),
            functions=[
                {
                    "script_score": {
                        "script": {
                            # using function_score query helps us to boost exact matches using keyword field which is our name fields
                            "source": """ 
                                    double score = 0;
                                    if (doc['name.keyword'].value == params.query) score += 10;
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
            # Use size and page for pagination.
        ).extra(size=size, from_=(page - 1) * size)
        results = search.execute()
        query_results = [{"id": hit.meta.id, "name": hit.name, "score": hit.meta.score} for hit in results]
        return query_results

    def find_by_id(self, pk: int) -> AgentDocument:
        """
        Find an Agent document by its ID.
        :param pk: Primary key of the property
        """
        try:
            agent_document = AgentDocument.get(id=str(pk))
            return agent_document
        except NotFoundError:
            raise AgentNotFound()

    def update(self, pk: int, updates: Dict[str, Any]) -> Tuple[AgentDocument, bool]:
        """
        Update an existing Agent document in Elasticsearch.
        :param pk: Primary key of the property
        :param updates: Dictionary of properties to update
        """
        agent_document = self.find_by_id(pk=pk)
        fields = list(updates.keys())
        agent_document, has_updated = DocumentUpdateService(document=agent_document, fields=fields, data=updates)
        return agent_document, has_updated

    def delete(self, pk: int):
        """
        Deletes an existing Agent document in Elasticsearch.
        :param pk: Primary key of the property
        """
        agent_instance = self.find_by_id(pk=pk)
        agent_instance.delete()
