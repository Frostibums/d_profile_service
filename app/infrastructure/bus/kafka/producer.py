import json
import logging

from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        await self._producer.stop()
