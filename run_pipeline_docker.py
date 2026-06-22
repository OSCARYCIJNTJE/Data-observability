import subprocess

def run(command, cwd=None):
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=cwd, check=True)

print("Starting Docker dbt pipeline...")

run(["python", "scripts/export_kafka_to_json.py"])
run(["python", "scripts/json_to_csv.py"])

dbt_project = "construction_elt_project"

run(["dbt", "seed", "--full-refresh"], cwd=dbt_project)
run(["dbt", "run"], cwd=dbt_project)
run(["dbt", "test"], cwd=dbt_project)
run(["dbt", "docs", "generate"], cwd=dbt_project)

print("Pipeline completed successfully.")