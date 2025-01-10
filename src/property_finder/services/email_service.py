import json
from typing import Any, Dict

from adapter.kafka import get_kafka_producer


class EmailService:
    def __init__(self):
        self.producer = get_kafka_producer()

    def send_email(self, body: Dict[str, Any]):
        self.producer.send(topic="email_topic", value=json.dumps(body))
