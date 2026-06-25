Write-Host "🚀 Starting Kafka → DuckDB → dbt pipeline"

$KafkaContainer = "kafka-kafka-1"
$Topic = "site-health-stream"
$JsonOutput = "site_health_events.json"
$DbtProject = "construction_elt_project"

Write-Host "1. Exporting Kafka topic to JSON..."

docker exec -i $KafkaContainer /opt/kafka/bin/kafka-console-consumer.sh `
  --bootstrap-server kafka:29092 `
  --topic $Topic `
  --from-beginning `
  --max-messages 10 > $JsonOutput

Write-Host "2. Converting JSON to CSV..."

Set-Location scripts
python json_to_csv.py
Set-Location ..

Write-Host "3. Running dbt seed..."

Set-Location $DbtProject
dbt seed --full-refresh

Write-Host "4. Running dbt models..."

dbt run

Write-Host "5. Running dbt tests..."

dbt test

Write-Host "6. Generating dbt docs..."

dbt docs generate

Set-Location ..

Write-Host "✅ Pipeline completed successfully"