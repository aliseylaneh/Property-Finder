from typing import Any, Dict, List

from src.property_finder.models import Agent
from src.property_finder.models.events.events import DeleteEvent, DomainEventTypes, UpdateEvent
from src.property_finder.repositories.django.agent import AgentDjangoRepository
from src.property_finder.repositories.es.es_agent import AgentElasticSearchRepository
from src.property_finder.tasks.tasks import async_delete_event, async_update_event


class AgentService:
    def __init__(self):
        """
        This service requires two dependencies
        1. A DjangoRepository that does all CRUD operations relevant to an Agent Django model.
        2. An ElasticsearchRepository which takes care of all CRUD operations relevant to an Agent Elasticsearch Document.
        """
        self._django_repository = AgentDjangoRepository()
        self._elastic_repository = AgentElasticSearchRepository()

    def find_agent(self, pk: int):
        """
        Finds an existing Agent
        :param pk: Agent ID.
        """
        return self._django_repository.find_by_id(pk=pk)

    def create_agent(self, name: str, email: str, phone_number: str) -> Agent:
        """
        Create a new Agent on both PostgreSQL and ElasticSearch, there reason is because Elasticsearch and PostgreSQL
        must be consistence upon creation and the source of truth for an Instance is PostgreSQL.
        :param name: The name of the agent
        :param email: The email address of the agent
        :param phone_number: The phone number of the agent
        """
        # Creating new instance of an Agent in PostgreSQL using Django repository.
        agent_instance = self._django_repository.create(name=name, email=email, phone_number=phone_number)
        # Creating new instance of an Agent in Elasticsearch using Elasticsearch repository.
        self._elastic_repository.index(pk=agent_instance.pk, name=name, email=email, phone_number=phone_number)
        return agent_instance

    def update_agent(self, pk: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates are done by elasticsearch repository, because where ever we update an item we expect the user
        to see the updated information when they are searching through properties, then we run Celery task to
        in order to update the PostgreSQL as source of truth.
        :param pk: Agent id.
        :param updates: A dictionary of values for dedicated fields of an Agent.
        """
        agent_document, has_updated = self._elastic_repository.update(pk=pk, updates=updates)

        # Update happens in PostgreSQL if and only the document fields has been updated.
        if has_updated:
            # Updating Agent in asynchronous matter for PostgresSQL.
            # Update event is also logged in Kafka topic.
            event = UpdateEvent(
                pk=pk,
                updates=updates,
                repo_name=AgentDjangoRepository.__name__,
                event_type=DomainEventTypes.AGENT_UPDATED
            ).model_dump()
            async_update_event.delay(event=event)
        return agent_document.to_dict()

    def delete_agent(self, pk: int):
        """
        This service will delete an Agent from ElasticSearch database by using AgentElasticSearchRepository.
        Then it will publish an event on Kafka in order to delete the data on PostgresSQL later.
        :param pk: Agent id.
        """
        self._elastic_repository.delete(pk=pk)

        # Deleting an Agent in asynchronous matter from PostgreSQL.
        # Delete event is also logged in Kafka topic.
        event = DeleteEvent(
            pk=pk,
            repo_name=AgentDjangoRepository.__name__,
            event_type=DomainEventTypes.AGENT_DELETED
        ).model_dump()
        async_delete_event(event=event)

    def search_agents(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Search the given query.
        :param query: Query will be the prompt for searching through the Agents,
        and it only includes Agent ID and name.
        """
        query = self._elastic_repository.search(query=query, **kwargs)
        return query
