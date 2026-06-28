from pathlib import Path
import json
import csv

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "site_health_events.json"
OUTPUT_FILE = BASE_DIR / "construction_elt_project" / "seeds" / "site_health_events.csv"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "site_id",
    "event_type",
    "severity",
    "score",
    "description",
    "timestamp"
]

def get_value(record, *keys):
    for key in keys:
        value = record.get(key)
        if value is not None:
            return value
    return None

rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    content = infile.read().strip()

    if content.startswith("["):
        records = json.loads(content)
    else:
        records = []
        for line in content.splitlines():
            line = line.strip()

            if not line or line.startswith("Processed a total"):
                continue

            records.append(json.loads(line))

    for record in records:
        rows.append({
            "site_id": get_value(record, "siteId", "site_id", "SITEID"),
            "event_type": get_value(record, "eventType", "event_type", "type", "TYPE", "EVENTTYPE"),
            "severity": get_value(record, "severity", "SEVERITY", "level", "riskLevel"),
            "score": get_value(record, "score", "SCORE", "riskScore"),
            "description": get_value(record, "description", "DESCRIPTION", "message"),
            "timestamp": get_value(record, "timestamp", "TIMESTAMP")
        })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Converted {len(rows)} records to {OUTPUT_FILE}")