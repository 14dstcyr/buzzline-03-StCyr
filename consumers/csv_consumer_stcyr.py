"""
csv_consumer_stcyr.py
Consume earthquake-like CSV-derived messages and detect seismic alerts.
"""

from __future__ import annotations
import os
import json
from collections import deque
from datetime import datetime

from utils.utils_logger import logger
from utils.utils_consumer import create_kafka_consumer


TOPIC = os.getenv("KAFKA_TOPIC_CSV_STCYR", "csv_stcyr")
GROUP_ID = os.getenv("KAFKA_GROUP_CSV_STCYR", "stcyr_csv_group")

# Alert thresholds
MAG_HIGH = float(os.getenv("MAG_HIGH_ALERT", "5.0"))
DELTA_SPIKE = float(os.getenv("MAG_DELTA_ALERT", "1.0"))
ROLLING_WINDOW = int(os.getenv("ROLLING_WINDOW", "5"))


def parse_ts(ts_str: str) -> datetime:
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        try:
            return datetime.fromisoformat(ts_str)
        except Exception:
            return datetime.now()


def main() -> None:
    logger.info(f"[CSV Consumer] Subscribing to topic: {TOPIC} (group: {GROUP_ID})")

    consumer = create_kafka_consumer(
        topic_provided=TOPIC,
        group_id_provided=GROUP_ID,
        value_deserializer_provided=lambda b: json.loads(b.decode("utf-8")),
    )

    last_mag = None
    recent_mags = deque(maxlen=ROLLING_WINDOW)

    try:
        for msg in consumer:
            record = msg.value  # {'timestamp': str, 'magnitude': float, ...}
            ts = parse_ts(str(record.get("timestamp", "")))
            mag = float(record.get("magnitude", "nan"))
            recent_mags.append(mag)

            # Streaming analytics
            alerts = []
            if mag >= MAG_HIGH:
                alerts.append(f"Magnitude ≥ {MAG_HIGH}")

            if last_mag is not None:
                delta = mag - last_mag
                if abs(delta) >= DELTA_SPIKE:
                    alerts.append(f"Aftershock Δ={delta:+.2f}")

            last_mag = mag
            avg = sum(recent_mags) / len(recent_mags)

            if alerts:
                logger.warning(f"[CSV Consumer][ALERT] {ts} mag={mag:.2f} avg={avg:.2f} | {', '.join(alerts)}")
            else:
                logger.info(f"[CSV Consumer] {ts} mag={mag:.2f} avg={avg:.2f}")

    except KeyboardInterrupt:
        logger.info("[CSV Consumer] Stopping (Ctrl+C).")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
