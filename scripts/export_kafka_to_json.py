import json
import os
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "site-health-stream")
OUTPUT_FILE = os.getenv("KAFKA_EXPORT_FILE", "site_health_events.json")
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "10"))

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id=None,
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print(f"Exporting from topic: {TOPIC}")
print(f"Bootstrap servers: {BOOTSTRAP_SERVERS}")
print(f"Max messages: {MAX_MESSAGES}")

count = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for message in consumer:
        json.dump(message.value, outfile)
        outfile.write("\n")

        count += 1

        if count >= MAX_MESSAGES:
            break

consumer.close()

print(f"Exported {count} messages to {OUTPUT_FILE}")