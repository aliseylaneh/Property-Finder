import threading

from kafka import TopicPartition

from adapter.kafka import KafkaGroupID, KafkaTopics
from property_finder.tasks.tasks import logger
from src.property_finder.repositories.django import *  # noqa This is requried in order to have classes loaded in our globals()
from src.property_finder.services.kafka_service import ProxyConsumerKafkaService


class ProcessUpdateEvents(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @staticmethod
    def _process_events(records: Dict[Any, Any]) -> Dict[str, Any] | None:
        """
        Process the records within a partition to get the most valuable data depending on our
        settings for TopicPartition.
        :param records: Latest event in the topic.
        """
        try:
            topic_partition = TopicPartition(topic="PostgresModelUpdateTopic", partition=0)
            consumer_record = records[topic_partition][0]
            event = consumer_record.value
            return event
        except KeyError:
            return None

    def run(self):
        """
        This scheduled async task will consume update events from KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
        and process them depending on their repository. It's essential to give group_id for consumers
        and producers to kafka it will be able to commit the process offsets.
        """
        try:
            with ProxyConsumerKafkaService(topic_name=KafkaTopics.POSTGRES_MODEL_UPDATE_TOPIC,
                                           group_id=KafkaGroupID.SCHEDULED_UPDATES) as consumer:
                while True:
                    event = self._process_events(consumer.poll(timeout_ms=2, max_records=1))
                    if not event:
                        continue
                    repository = globals()[event['repo_name']]
                    repository().update(pk=int(event['pk']), updates=event['updates'])
        except Exception as exception:
            logger.error(exception)
