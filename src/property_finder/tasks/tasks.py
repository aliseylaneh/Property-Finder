import logging
from typing import Any, Dict

from django_redis_task_lock import lock

from adapter.celery import celery
from adapter.kafka import KafkaGroupID, KafkaTopics
from config.settings.celery import CELERY_TASK_LOCK_CACHE
from property_finder.models.exceptions.events import EventNotFound

logger = logging.getLogger(__name__)


@celery.task
def send_updates_event(event: Dict[str, Any]):
    from property_finder.services.kafka_service import ProxyProducerKafkaService
    """
    This async task is responsible for sending updates of a Django model to its dedicated topic,
    So it will be consumed later on and process depending on repository.
    :param event: An event dictionary which is going to be produced on kafka
    """
    with ProxyProducerKafkaService() as producer:
        producer.send(topic=KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC, key=None, value=event)


# @celery.task(soft_time_limit=120, time_limit=150, autoretry_for=(EventNotFound,), )
# @lock(timeout=30, cache=CELERY_TASK_LOCK_CACHE, lock_name='process_update_events')
# def process_update_events():
#     from property_finder.services.kafka_service import ProxyConsumerKafkaService
#     """
#     This scheduled async task will consume update events from KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
#     and process them depending on their repository. It's essential to give group_id for consumers
#     and producers to kafka it will be able to commit the process offsets.
#     """
#     with ProxyConsumerKafkaService(topic_name=KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
#                                    group_id=KafkaGroupID.SCHEDULED_UPDATES) as consumer:
#         record = next(consumer)
#         event = record.value
#         if event:
#             logger.info("Processing update event")
#             repository = globals()[event['repo_name']]
#             repository().update(pk=int(event['pk']), updates=event['updates'])
#         else:
#             raise EventNotFound()
