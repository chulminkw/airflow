from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime
import io

# DAG definition
with DAG(
    dag_id="minio_s3hook_example",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["minio", "s3hook"],
) as dag:

    # Task: upload a file to MinIO
    def upload_to_minio():
        hook = S3Hook(aws_conn_id="minio_default")  # must match your connection ID
        data = "Hello from S3Hook to MinIO!"
        bucket_name = "mybucket"
        key = "example/demo.txt"
        
        # Make sure bucket exists
        hook.create_bucket(bucket_name)
        
        # Upload string as object
        hook.load_string(string_data=data, key=key, bucket_name=bucket_name, replace=True)
        print(f"Uploaded '{key}' to bucket '{bucket_name}'")

    upload_task = PythonOperator(
        task_id="upload_to_minio",
        python_callable=upload_to_minio,
    )

    # Task: download/read the file from MinIO
    def read_from_minio():
        hook = S3Hook(aws_conn_id="minio_default")
        bucket_name = "mybucket"
        key = "example/demo.txt"
        
        content = hook.read_key(key=key, bucket_name=bucket_name)
        print(f"Content from MinIO: {content}")

    read_task = PythonOperator(
        task_id="read_from_minio",
        python_callable=read_from_minio,
    )

    upload_task >> read_task
