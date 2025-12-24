from airflow.sdk import DAG, Asset, task
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from pendulum import datetime

local_file_asset = [Asset("simple_my_local")]
LOCAL_PATH = "/usr/local/airflow/include/user_data/simple.txt"

with DAG(
    dag_id="create_simple_file_producer",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False
) as simple_file_producer_dag:
    
    @task(outlets=local_file_asset)
    def create_local_file():
        import pandas as pd
        df = pd.DataFrame({
            "order_id": [10, 20, 30],
            "amount": [100, 200, 300]
        })
        df.to_csv(LOCAL_PATH, index=False)
        return LOCAL_PATH
    
    create_local_task = create_local_file()


with DAG(
    dag_id="local_to_s3_by_asset",
    start_date=datetime(2025, 12, 1),
    schedule=local_file_asset,
    catchup=False
) as dag:
    
    # filename은 로컬 파일명, dest_key
    upload_to_minio_op = LocalFilesystemToS3Operator(
        task_id="upload_local_file",
        filename=LOCAL_PATH, # filename은 로컬 파일명
        dest_key="demo/simple.txt", # dest_bucket 밑에 저장될 sub folder/파일명
        dest_bucket="mybucket", # load될 bucket 명
        # aws_conn_id="minio_conn" # 아이디/패스워드 권한을 통한 connection
        aws_conn_id="minio_accesskey_conn", # access key를 통한 connection
        replace=True # bucket에 해당 파일이 있으면 replace 수행. default는 False
    )