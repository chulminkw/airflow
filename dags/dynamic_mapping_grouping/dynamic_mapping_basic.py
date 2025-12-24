from airflow.sdk import DAG, task
from pendulum import datetime

with DAG(
    dag_id="d_mapping_basic",
    schedule=None,
    start_date=datetime(2025, 12, 1),
    catchup=False
) as dag:
    
    @task
    def list_files():
        return ["a.csv", "b.csv", "c.csv"]
    
    @task
    def process_file(filename):
        print(f"##### filename: {filename}")

    files = list_files()
    # expand()의 인자로 iterable(예: list) 이 입력됨
    process_file.expand(filename=files)