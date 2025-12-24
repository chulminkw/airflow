from airflow.sdk import DAG, task
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from pendulum import datetime

LOCAL_PATH = "/home/astro/data_01.csv"

with DAG(
    dag_id="s3_sensor_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    s3_key_sensor = S3KeySensor(
        task_id="s3_key_sensor_01",
        bucket_key="incoming/data_01.csv",
        bucket_name="mybucket",
        aws_conn_id="minio_conn",
        poke_interval=30,
        timeout=60*60,
        mode="reschedule"
    )

    @task
    def download_to_local(): 
        #S3Hook을 사용하여 local file로 Download 수행. 
        hook = S3Hook(aws_conn_id="minio_conn")
        hook.download_file(
            key="incoming/data_01.csv",
            bucket_name="mybucket",
            local_path=LOCAL_PATH,
            preserve_file_name=True
        )
        return LOCAL_PATH

    @task
    def read_file(local_path):
        print(f"####### local_path:{local_path}")
        with open(local_path) as f:
            content = f.read()
        print("====== File Content =======")
        print(content)

    download_to_local_task = download_to_local()
    read_file_task = read_file(download_to_local_task)
    
    s3_key_sensor >> download_to_local_task >> read_file_task
