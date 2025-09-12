"""
json_consumer_stcyr.py
Consume earthquake JSON messages and run real-time analytics/alerts.
"""

from __future__ import annotations
import os
import json

from utils.utils_logger import logger
from utils.utils_consumer import create_kafka_consumer


TOPIC = os.getenv("KAFKA_TOPIC_JSON_STCYR", "json_stcyr")
GROUP_ID = os.getenv("KAFKA_GROUP_JSON_STCYR", "stcyr_json_group")


def alert_logic(record: dict) -> None:
    """
    Alert if:
    - Category is 'aftershock'
    - Message contains 'aftershock' or 'magnitude'
    """
    text = str(record.get("message", "")).lower()
    category = str(record.get("category", "")).lower()

    if "aftershock" in text or "magnitude" in text or category == "aftershock":
        logger.warning(f"[JSON Consumer][ALERT] {record}")
    else:
        logger.info(f"[JSON Consumer] ok -> {record}")


def main() -> None:
    logger.info(f"[JSON Consumer] Subscribing to topic: {TOPIC} (group: {GROUP_ID})")

    consumer = create_kafka_consumer(
        topic_provided=TOPIC,
        group_id_provided=GROUP_ID,
        value_deserializer_provided=lambda b: json.loads(b.decode("utf-8")),
    )

    try:
        for msg in consumer:
            record = msg.value
            alert_logic(record)

    except KeyboardInterrupt:
        logger.info("[JSON Consumer] Stopping (Ctrl+C).")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
