"""
csv_producer_stcyr.py
Stream CSV rows as JSON earthquake-like events to a Kafka topic.
"""

from __future__ import annotations
import os
import json
import time
from datetime import datetime, timedelta
from typing import Iterable, Dict

from kafka import KafkaProducer

from utils.utils_logger import logger
from utils.utils_producer import get_kafka_broker_address


TOPIC = os.getenv("KAFKA_TOPIC_CSV_STCYR", "csv_stcyr")
SLEEP_SECS = float(os.getenv("PRODUCER_SLEEP_SECS", "0.75"))
CSV_SOURCE_FILE = os.getenv("CSV_SOURCE_FILE", "")


def iter_csv_rows() -> Iterable[Dict]:
    """
    Yield rows as dicts with keys: timestamp (str), magnitude (float).
    If no CSV file is given, generate synthetic tremor readings.
    """
    if CSV_SOURCE_FILE and os.path.exists(CSV_SOURCE_FILE):
        import csv
        with open(CSV_SOURCE_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield {
                    "timestamp": row["timestamp"],
                    "magnitude": float(row["magnitude"]),
                    "source": "file",
                }
        return

    # Synthetic fallback
    logger.info("[CSV Producer] No CSV_SOURCE_FILE provided — generating synthetic seismic data.")
    start = datetime.now().replace(second=0, microsecond=0)
    mag = 2.0
    for i in range(20):
        ts = (start + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
        if i in (7, 14):  # simulate spikes
            mag += 1.5
        else:
            mag += 0.2
        yield {"timestamp": ts, "magnitude": round(mag, 2), "source": "synthetic"}


def main() -> None:
    broker = get_kafka_broker_address()
    logger.info(f"[CSV Producer] Connecting to broker at: {broker}")
    logger.info(f"[CSV Producer] Topic: {TOPIC}")

    producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        linger_ms=50,
        acks="all",
    )

    try:
        for record in iter_csv_rows():
            producer.send(TOPIC, value=record)
            logger.info(f"[CSV Producer] sent -> {record}")
            time.sleep(SLEEP_SECS)

        # Continuous tremor signals
        i = 0
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mag = 2.5 + (i % 5) * 0.3
            record = {"timestamp": now, "magnitude": round(mag, 2), "source": "tremor"}
            producer.send(TOPIC, value=record)
            logger.info(f"[CSV Producer] sent -> {record}")
            time.sleep(SLEEP_SECS)
            i += 1

    except KeyboardInterrupt:
        logger.info("[CSV Producer] Stopping (Ctrl+C).")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
