import datetime
import json
import logging
from typing import Any
from uuid import uuid4

from aiokafka import AIOKafkaConsumer

from app.config.kafka import kafka_settings
from app.domain.entities.profile import Profile
from app.infrastructure.di.container import Container

container: Container = Container()
logger = logging.getLogger(__name__)


async def start_kafka_consumer():
    try:
        logger.info("Kafka consumer started")
        await consume_user_events()
    except Exception as e:
        logger.error("Kafka consumer crashed: %s", str(e))


async def handle_user_created(data: dict[str, Any]) -> None:
    logger.info(f"User created event: {data}")
    async with container.get_session() as session:
        profile_service = container.get_profile_service(session)
        profile = Profile(
            id=uuid4(),
            user_id=data.get("user_id"),
            created_at=datetime.datetime.utcnow(),
        )
        logger.info("Creating profile: %s", profile)
        await profile_service.create(profile)
        logger.info("Created profile for user_id: %s (%s)", profile.user_id, profile.id)


async def consume_user_events():
    event_handlers_map = {
        "user_created": handle_user_created,
    }
    consumer = AIOKafkaConsumer(
        "user-events",
        bootstrap_servers=kafka_settings.bootstrap_servers,
        group_id="profile-service",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()

    try:
        async for msg in consumer:
            data = msg.value
            handler_func = event_handlers_map.get(data.get("event"))
            if handler_func:
                await handler_func(data)
    finally:
        await consumer.stop()
