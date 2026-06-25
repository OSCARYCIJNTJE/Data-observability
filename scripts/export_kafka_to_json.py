import os
import json
from kafka import KafkaConsumer

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
topic = os.getenv("KAFKA_TOPIC", "site-health-stream")
output_file = os.getenv("KAFKA_EXPORT_FILE", "site_health_events.json")
max_messages = int(os.getenv("MAX_MESSAGES", "10"))
consumer_timeout_ms = int(os.getenv("CONSUMER_TIMEOUT_MS", "60000"))

print(f"Connecting to Kafka: {bootstrap_servers}", flush=True)
print(f"Reading topic: {topic}", flush=True)
print(f"Max messages: {max_messages}", flush=True)

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="dbt-pipeline-ci",
    consumer_timeout_ms=consumer_timeout_ms,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

events = []

for message in consumer:
    events.append(message.value)
    print(f"Consumed message {len(events)}/{max_messages}", flush=True)

    if len(events) >= max_messages:
        break

consumer.close()

print(f"Finished consuming. Total messages: {len(events)}", flush=True)

if len(events) == 0:
    raise RuntimeError("No Kafka messages were consumed. Producer may not be writing to the expected topic.")

with open(output_file, "w") as f:
    json.dump(events, f, indent=2)

print(f"Wrote events to {output_file}", flush=True)