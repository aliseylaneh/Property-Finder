from typing import Any, Dict, List

from elasticsearch import NotFoundError
from elasticsearch_dsl.query import Q

from src.property_finder.es.documents.agent import AgentDocument
from src.property_finder.models.exceptions.agent import AgentNotFound
from src.property_finder.repositories import AbstractRepository


class AgentElasticSearchRepository(AbstractRepository):

    def index(self, pk: int, name: str, email: str, phone_number: str):
        pass

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

    def update(self, *args, **kwargs):
        pass

    def delete(self, pk: str):
        try:
            agent_instance = AgentDocument.get(id=pk)
            agent_instance.delete()
        except NotFoundError:
            raise AgentNotFound()
