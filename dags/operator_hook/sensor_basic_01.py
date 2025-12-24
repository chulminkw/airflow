from airflow.sdk import DAG, task
from airflow.providers.standard.sensors.filesystem import FileSensor
from pendulum import datetime

LOCAL_FILE_PATH = "/home/astro/testdata.txt"

with DAG(
    dag_id="file_sensor_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    local_file_sensor = FileSensor(
        task_id="local_file_sensor",
        filepath=LOCAL_FILE_PATH,
        poke_interval=30,
        timeout=60*60, # 1 hour
        fs_conn_id="fs_default", # airflow 2.7 이후 지정 필요.
        mode="reschedule" # poke 수행 후 worker slot release
    )

    @task
    def read_file():
        with open(LOCAL_FILE_PATH) as f:
            content = f.read()
        print("====== File Content =======")
        print(content)

    read_file_task = read_file()
    
    local_file_sensor >> read_file_task

    # @task
    # def process_file():
    #     print("process the file now")

    # local_file_sensor >> process_file
    
