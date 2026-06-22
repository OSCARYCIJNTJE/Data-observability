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

rows = []

with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()

        if not line or line.startswith("Processed a total"):
            continue

        record = json.loads(line)

        rows.append({
            "site_id": record.get("SITEID"),
            "event_type": record.get("EVENTTYPE"),
            "severity": record.get("SEVERITY"),
            "score": record.get("SCORE"),
            "description": record.get("DESCRIPTION"),
            "timestamp": record.get("TIMESTAMP")
        })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Converted {len(rows)} records to {OUTPUT_FILE}")