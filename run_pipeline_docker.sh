#!/bin/bash
set -e

echo "🚀 Starting Kafka → DuckDB → dbt pipeline"

echo "1. Exporting Kafka topic to JSON..."

kafka-console-consumer.sh \
  --bootstrap-server kafka:29092 \
  --topic site-health-stream \
  --from-beginning \
  --max-messages 10 > site_health_events.json

echo "2. Converting JSON to CSV..."

cd scripts
python json_to_csv.py
cd ..

echo "3. Running dbt..."

cd construction_elt_project
dbt seed --full-refresh
dbt run
dbt test
dbt docs generate

echo "✅ dbt pipeline completed"