from datetime import datetime
from confluent_kafka import Producer
from app.config import settings
import json


class KafkaLogger:
    def __init__(self):
        self.producer = Producer({"bootstrap.servers": settings.KAFKA_BROKER})

    def log_action(self, action: str, details):
        if isinstance(details, dict):
            if 'date' in details:
                details['date'] = details['date'].isoformat()
        message = {
            "action": action,
            "details": details,
            "date": datetime.now().isoformat()
        }
        self.producer.produce(settings.KAFKA_TOPIC,
                              json.dumps(message).encode("utf-8"))
        self.producer.flush()


kafka_logger = KafkaLogger()
