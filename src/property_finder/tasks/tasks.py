import logging

from kafka.errors import NoBrokersAvailable, KafkaError

from adapter.celery import celery
from adapter.kafka import KafkaTopics
from src.property_finder.services.kafka_service import ProxyProducerKafkaService
from src.property_finder.repositories.django import *  # noqa

logger = logging.getLogger(__name__)


@celery.task(bind=True,
             autoretry_for=(NoBrokersAvailable, KafkaError),
             retry_backoff=10,
             max_retries=10)
def async_publish_postgres_event(self, pk: int, event_type: str):
    """
    This will publish any kind of event that happened through our code for models.
    :param pk: Would be a model primary key
    :param event_type: Type of event that happened.
    """
    with ProxyProducerKafkaService() as producer:
        producer.send(
            topic=KafkaTopics.POSTGRES_EVENT_LOGS_TOPIC, key=None,
            value={'pk': pk, 'event_type': event_type}
        ).get(timeout=10)


@celery.task(bind=True,
             autoretry_for=(NoBrokersAvailable, KafkaError),
             retry_backoff=10,
             max_retries=10)
def async_update_event(self, event: Dict[str, Any]):
    """
    This async task is responsible for sending updates of a Django model to its dedicated topic,
    So it will be consumed later on and process depending on repository.
    :param event: An event dictionary which is going to be produced on kafka
    """
    repository = globals()[event['repo_name']]
    instance = repository().update(pk=int(event['pk']), updates=event['updates'])
    async_publish_postgres_event.delay(pk=instance.pk, event_type=event['event_type'])


@celery.task(bind=True,
             autoretry_for=(NoBrokersAvailable, KafkaError),
             retry_backoff=10,
             max_retries=10)
def async_delete_event(self, event: Dict[str, Any]):
    """
    This async task is responsible for sending updates of a Django model to its dedicated topic,
    So it will be consumed later on and process depending on repository.
    :param event: An event dictionary which is going to be produced on Kafka.
    """
    repository = globals()[event['repo_name']]
    repository().delete(pk=int(event['pk']))
    async_publish_postgres_event.delay(pk=event['pk'], event_type=event['event_type'])


@celery.task(bind=True,
             autoretry_for=(NoBrokersAvailable, KafkaError),
             retry_backoff=10,
             max_retries=10)
def async_send_email(self, property_title: str, agent_email: str):
    """
    This function publishes an email in an asynchronous matter to Kafka topic EMAIL_TOPIC, and
    it's implemented to send email in upon creation of a Property instance. so later on it could
    be consumed by any type of process.
    :param property_title: Property title.
    :param agent_email: Email of an Agent which is associated with Property.
    """
    with ProxyProducerKafkaService() as producer:
        producer.send(
            topic=KafkaTopics.EMAIL_TOPIC, key=None,
            value={"property_title": property_title, "agent_email": agent_email}
        ).get(timeout=10)
