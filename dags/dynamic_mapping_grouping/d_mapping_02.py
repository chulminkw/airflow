from airflow.sdk import DAG
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from pendulum import datetime

with DAG(
    dag_id="dynamic_mapping_s3_sensor",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
):

    files = [
        "incoming/data1.csv",
        "incoming/data2.csv",
        "incoming/data3.csv",
    ]
    # 3개의 S3KeySensor용 sensor task가 동작하며, 
    # 개별 task들은 각각 data1.csv, data2.csv, data3.csv를 모니터링함. 
    S3KeySensor.partial(
        task_id="wait_for_files",
        bucket_name="mybucket",
        aws_conn_id="minio_accesskey_conn",
        poke_interval=10,
    ).expand(
        bucket_key=files
    )