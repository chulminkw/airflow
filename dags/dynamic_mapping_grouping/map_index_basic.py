from airflow.sdk import DAG, task, get_current_context
from pendulum import datetime

with DAG(
    dag_id="map_index_basic",
    schedule=None,
    start_date=datetime(2025, 12, 1),
    catchup=False
) as dag:
    
    @task
    def list_files():
        return ["a.csv", "b.csv", "c.csv"]
    
    @task
    def process_file(filename):
        # map_index값은 task내에서 참조 될 수 있으며, 
        # 이를 위해 get_current_context()로 context를 가져와서 map_index값을 추출
        context = get_current_context()
        map_index = context["ti"].map_index
        print(f"#### processing file: {filename}, map_index={map_index}")

    files = list_files()
    # expand()의 인자로 iterable(예: list) 이 입력됨
    process_file.expand(filename=files)