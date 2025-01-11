import logging

from adapter.celery import celery
from adapter.kafka import KafkaGroupID, KafkaTopics
from property_finder.services.kafka_service import ProxyConsumerKafkaService, ProxyProducerKafkaService
from src.property_finder.repositories.django import *  # noqa This is requried in order to have classes loaded in our globals()

logger = logging.getLogger(__name__)


@celery.task
def send_updates_event(event: Dict[str, Any]):
    """
    This async task is responsible for sending updates of a Django model to its dedicated topic,
    So it will be consumed later on and process depending on repository.
    :param event: An event dictionary which is going to be produced on kafka
    """
    with ProxyProducerKafkaService(group_id=KafkaGroupID.SCHEDULED_UPDATES) as producer:
        producer.send(topic=KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC, key=None, value=event)


def process_update_event():
    """
    This scheduled async task will consume update events from KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
    and process them depending on their repository. It's essential to give group_id for consumers
    and producers to kafka it will be able to commit the process offsets.
    """
    with ProxyConsumerKafkaService(topic_name=KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
                                   group_id=KafkaGroupID.SCHEDULED_UPDATES) as consumer:
        record = next(consumer)
        event = record.value
        if event:
            repository = globals()[event['repo_name']]
            repository().update(pk=int(event['pk']), updates=event['updates'])
