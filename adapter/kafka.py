import json
from enum import StrEnum

from kafka import KafkaConsumer, KafkaProducer

from config.django.base import KAFKA_BOOTSTRAP_SERVERS


class KafkaTopics(StrEnum):
    POSTGRES_EVENT_LOGS_TOPIC = "PostgresEventLogsTopic"
    EMAIL_TOPIC = "EmailTopic"


class KafkaGroupID(StrEnum):
    SCHEDULED_UPDATES = "ScheduledUpdates"


def get_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
    )
    return producer


def get_kafka_consumer(topic_name: str, group_id: str):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
    )
    return consumer
