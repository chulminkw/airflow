from airflow.sdk import DAG
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from pendulum import datetime

# 로컬 파일은 worker가 수행되는 scheduler 서버의 파일이어야 함. api-server 아님. 
LOCAL_FILE = "/usr/local/airflow/README.md" #"/home/astro/upload_test.txt"

with DAG(
    dag_id="s3_operator_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    # filename은 로컬 파일명, dest_key
    upload_to_minio_op = LocalFilesystemToS3Operator(
        task_id="upload_local_file",
        filename=LOCAL_FILE, # filename은 로컬 파일명
        dest_key="demo/upload_test.txt", # dest_bucket 밑에 저장될 sub folder/파일명
        dest_bucket="mybucket", # load될 bucket 명
        # aws_conn_id="minio_conn" # 아이디/패스워드 권한을 통한 connection
        aws_conn_id="minio_accesskey_conn", # access key를 통한 connection
        replace=True # bucket에 해당 파일이 있으면 replace 수행. default는 False
    )

    upload_to_minio_op