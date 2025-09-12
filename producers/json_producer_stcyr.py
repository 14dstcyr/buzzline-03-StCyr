"""
json_producer_stcyr.py
Send custom JSON "earthquake" messages to a Kafka topic.
"""

from __future__ import annotations
import os
import json
import time
from typing import Dict, List

from kafka import KafkaProducer

from utils.utils_logger import logger
from utils.utils_producer import get_kafka_broker_address


# ---------- Config ----------
TOPIC = os.getenv("KAFKA_TOPIC_JSON_STCYR", "json_stcyr")
SLEEP_SECS = float(os.getenv("PRODUCER_SLEEP_SECS", "1.0"))


def get_messages() -> List[Dict]:
    """
    Initial batch of themed messages.
    """
    return [
        {"message": "Minor tremor detected near station A.", "author": "SensorBot", "category": "tremor"},
        {"message": "Seismic waveforms stable.", "author": "Analyst", "category": "status"},
        {"message": "AFTERSHOCK detected magnitude 3.2", "author": "OpsBot", "category": "aftershock"},
        {"message": "Seismic monitoring active.", "author": "Deb", "category": "status"},
    ]


def main() -> None:
    broker = get_kafka_broker_address()
    logger.info(f"[JSON Producer] Connecting to broker at: {broker}")
    logger.info(f"[JSON Producer] Topic: {TOPIC}")

    producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=50,
        acks="all",
    )

    try:
        # Send starter batch
        for msg in get_messages():
            producer.send(TOPIC, value=msg)
            logger.info(f"[JSON Producer] sent -> {msg}")
            time.sleep(SLEEP_SECS)

        # Ongoing tremor signals
        i = 0
        while True:
            msg = {
                "message": f"Tremor signal #{i}",
                "author": "Deb",
                "category": "tremor"
            }
            producer.send(TOPIC, value=msg)
            logger.info(f"[JSON Producer] sent -> {msg}")
            time.sleep(SLEEP_SECS)
            i += 1

    except KeyboardInterrupt:
        logger.info("[JSON Producer] Stopping (Ctrl+C).")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
