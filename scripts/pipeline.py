import pandas as pd
import os
import json
from datetime import datetime

# -----------------------------
# BASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data/raw/orders_bad.csv")
CLEAN_PATH = os.path.join(BASE_DIR, "data/clean/clean_data.csv")
QUARANTINE_PATH = os.path.join(BASE_DIR, "data/quarantine/quarantined.csv")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

# -----------------------------
# REQUIRED SCHEMA
# -----------------------------
REQUIRED_COLUMNS = [
    "order_id",
    "customer_id",
    "amount",
    "country",
    "order_date"
]

# -----------------------------
# LOAD DATA
# -----------------------------
def load_data(path):
    print(f"\nLoading dataset: {path}")
    return pd.read_csv(path)

# -----------------------------
# VALIDATION
# -----------------------------
def validate_schema(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return len(missing) == 0, missing


def validate_data(df):
    errors = []

    if df["customer_id"].isnull().any():
        errors.append("Null customer_id")

    if (pd.to_numeric(df["amount"], errors="coerce") < 0).any():
        errors.append("Negative amount")

    return errors

# -----------------------------
# SELF HEALING
# -----------------------------
def self_heal(df):
    df = df.copy()

    df["country"] = df["country"].fillna("UNKNOWN")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["customer_id"])
    df = df[df["amount"] >= 0]
    after = len(df)

    return df, before - after

# -----------------------------
# METRICS
# -----------------------------
def compute_metrics(valid, invalid):
    ratio = float("inf") if invalid == 0 else valid / invalid
    return {
        "valid_rows": valid,
        "invalid_rows": invalid,
        "data_to_error_ratio": ratio
    }

# -----------------------------
# LOGGING
# -----------------------------
def save_log(run_id, log_data):
    file_path = os.path.join(LOG_DIR, f"run_{run_id}.json")

    with open(file_path, "w") as f:
        json.dump(log_data, f, indent=4)

    print(f"[LOG SAVED] {file_path}")

# -----------------------------
# PIPELINE EXECUTION
# -----------------------------
def run_pipeline(run_id):
    print(f"\n================ RUN {run_id} ================\n")

    df = load_data(DATA_PATH)

    schema_ok, missing = validate_schema(df)

    log = {
        "run_id": run_id,
        "timestamp": str(datetime.now()),
        "schema_ok": schema_ok,
        "missing_columns": missing,
        "errors": [],
        "metrics": {}
    }

    if not schema_ok:
        log["errors"].append(f"Missing columns: {missing}")
        save_log(run_id, log)
        return log

    errors = validate_data(df)
    log["errors"].extend(errors)

    if errors:
        df_healed, removed = self_heal(df)

        metrics = compute_metrics(len(df_healed), removed)
        log["metrics"] = metrics
        log["rows_removed_by_healing"] = removed

        df_healed.to_csv(CLEAN_PATH, index=False)

        print("[SELF-HEALING COMPLETE]")

    else:
        df.to_csv(CLEAN_PATH, index=False)
        log["metrics"] = compute_metrics(len(df), 0)

        print("[DATA CLEAN] No issues found")

    save_log(run_id, log)

    return log

# -----------------------------
# EXPERIMENT RUNNER
# -----------------------------
def run_experiment(n_runs=3):
    results = []

    for i in range(1, n_runs + 1):
        result = run_pipeline(i)
        results.append(result)

    summary = pd.DataFrame([
        {
            "run": r["run_id"],
            "valid_rows": r["metrics"].get("valid_rows", 0),
            "invalid_rows": r["metrics"].get("invalid_rows", 0),
            "data_to_error_ratio": r["metrics"].get("data_to_error_ratio", 0),
            "errors": len(r["errors"])
        }
        for r in results
    ])

    summary_path = os.path.join(LOG_DIR, "summary.csv")
    summary.to_csv(summary_path, index=False)

    print("\n================ SUMMARY ================")
    print(summary)
    print(f"\n[SUMMARY SAVED] {summary_path}")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_experiment(n_runs=3)