from typing import Any, Dict, List

from property_finder.models.events.events import DomainEventTypes, UpdateEvent, DeleteEvent
from src.property_finder.models import Property
from src.property_finder.repositories.django.agent import AgentDjangoRepository
from src.property_finder.repositories.django.property import PropertyDjangoRepository
from src.property_finder.repositories.django.property_type import PropertyTypeRepository
from src.property_finder.repositories.es.es_property import PropertyElasticSearchRepository
from src.property_finder.tasks.tasks import async_update_event, async_delete_event, async_send_email


class PropertyService:
    def __init__(self):
        """
        Property service provide all operations that are dedicated to Property domain model of our business.
        This service is actually the level of implementing logics between presentation layer and between domain layer.
        It's bind with two dependency one is PropertyDjangoRepository and one is PropertyElasticSearchRepository.
        """
        self._django_property_repository = PropertyDjangoRepository()
        self._elastic_property_repository = PropertyElasticSearchRepository()
        self._django_agent_repository = AgentDjangoRepository()
        self._property_type_repository = PropertyTypeRepository()

    def create_property(self, main_type, sub_type, title, description, agent) -> Property:
        """
        Create a new Property on both PostgreSQL and ElasticSearch, there reason is because Elasticsearch and PostgreSQL
        must be consistence upon creation and the source of truth for an Instance is PostgreSQL.
        :param main_type: Property type ID as main type of Property.
        :param sub_type: Property type ID as subtype of Property.
        :param title: Property title.
        :param description: Property description.
        :param agent: An Agent ID which will be associated to Property.
        """
        # Creating new instance using Django Repository of Property for saving on PostgreSQL
        property_instance = self._django_property_repository.create(
            main_type=main_type,
            sub_type=sub_type,
            title=title,
            description=description,
            agent=agent,
        )

        # Indexing on Elasticsearch the created instance.
        self._elastic_property_repository.index(
            pk=property_instance.pk,
            main_type={"id": property_instance.main_type.id, "title": property_instance.main_type.title},
            sub_type={"id": property_instance.sub_type.id, "title": property_instance.sub_type.title},
            title=title,
            description=description,
            agent={"id": property_instance.agent.id, "name": property_instance.agent.name}
        )

        # Sending an email including the property title an associated agent email into Kafka EMAIL_TOPIC
        async_send_email.delay(property_title=property_instance.title, agent_email=property_instance.agent.email)
        return property_instance

    def find_property(self, pk: int) -> Property:
        """
        Retrieve a Property instance from PostgreSQL.
        :param pk: Property id
        :return: Property instance
        """
        return self._django_property_repository.find_by_id(pk=pk)

    def _prepare_update_dict(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        This service is responsible to preparing dictionary for update operation in ElasticSearch.
        Validates assigned the Main type, Sub type and Agent ID by calling the PostgresSQL for ensuring
        data consistency.
        :param updates: Dictionary of updates
        :return: Dictionary of prepared updates ElasticSearch documents.
        """
        # Validating and retrieving Main and Sub type, due to the responsibility of PostgreSQL as source of truth.
        main_type, sub_type = self._property_type_repository.get_required_types(
            main_type=updates.get('main_type', None),
            sub_type=updates.get('sub_type', None)
        )

        # Validating and retrieving agent from PostgreSQL.
        agent = self._django_agent_repository.find_by_id(pk=updates.get('agent', None))

        # Assigning retrieved values to dict of updated fields.
        updates['main_type'] = main_type.to_dict()
        updates['sub_type'] = sub_type.to_dict()
        updates['agent'] = agent.to_dict()
        return updates

    def update_property(self, pk: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates are done by elasticsearch repository, because where ever we update an item we expect the user
        to see the updated information when they are searching through properties, then we run Celery task to
        in order to update the PostgreSQL as source of truth.
        :param pk: Property id
        :param updates: A dictionary of values for dedicated fields of Property
        """

        # Updating the property instance in Elasticsearch.
        prepared_updates = self._prepare_update_dict(updates.copy())
        property_instance = self._elastic_property_repository.update(pk=pk, updates=prepared_updates)

        # Updating property in asynchronous matter from PostgresSQL.
        # Update event is also logged in Kafka topic.
        event = UpdateEvent(
            pk=pk,
            updates=updates,
            repo_name=PropertyDjangoRepository.__name__,
            event_type=DomainEventTypes.PROPERTY_UPDATED
        ).model_dump()
        async_update_event.delay(event=event)
        return property_instance.to_dict()

    def delete_property(self, pk: int):
        """
        This service will delete Property from ElasticSearch database by using PropertyElasticSearchRepository.
        Then it will publish an event on Kafka in order to delete the data on PostgresSQL later.
        :param pk: Property id.
        """
        self._elastic_property_repository.delete(pk=pk)

        # Deleting property in asynchronous matter from PostgreSQL.
        # Delete event is also logged in Kafka topic.
        event = DeleteEvent(
            pk=pk,
            repo_name=PropertyDjangoRepository.__name__,
            event_type=DomainEventTypes.PROPERTY_DELETED
        ).model_dump()
        async_delete_event(event=event)

    def search_property(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Search the given query.
        :param query: Query will be the prompt for searching through the Properties,
        and it can include PropertyType titles and Property title
        """
        query = self._elastic_property_repository.search(query=query, **kwargs)
        return query
