from kafka import KafkaConsumer, KafkaProducer

from config.django.base import KAFKA_BOOTSTRAP_SERVERS


def get_kafka_producer():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    return producer


def get_kafka_consumer(topic_name: str):
    consumer = KafkaConsumer(topic_name, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    return consumer
