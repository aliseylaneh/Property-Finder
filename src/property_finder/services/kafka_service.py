from kafka import KafkaConsumer, KafkaProducer

from adapter.kafka import get_kafka_consumer, get_kafka_producer


class ProxyProducerKafkaService:

    def __enter__(self) -> KafkaProducer:
        self.producer = get_kafka_producer()
        return self.producer

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.producer:
            self.producer.close()


class ProxyConsumerKafkaService:
    def __init__(self, topic_name: str, group_id: str):
        self.topic_name = topic_name
        self.group_id = group_id

    def __enter__(self) -> KafkaConsumer:
        self.consumer = get_kafka_consumer(topic_name=self.topic_name, group_id=self.group_id)
        return self.consumer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.close()
