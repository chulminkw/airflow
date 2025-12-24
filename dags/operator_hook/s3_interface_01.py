from airflow.sdk import DAG, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from pendulum import datetime
import os

BUCKET_NAME = "mybucket"
AWS_CONN_ID = "minio_conn"
KEY_PREFIX = "sample/"
LOCAL_DIR = "/usr/local/airflow/include/user_data"

with DAG(
    dag_id="sample_s3_interface",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False
) as dag:
    
    #테스트용 local file을 /usr/local/airflow/include/user_data/ 디렉토리에 생성. 
    @task
    def create_local_file(filename):
        local_path = os.path.join(LOCAL_DIR, filename)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        # local file에는 간단한 내용을 기재하고 저장.
        with open(local_path, "w") as f:
            f.write(f"sample file is created at now")
        return local_path
    
    local_file_path = create_local_file("sample.txt")

    @task
    def upload_to_s3(local_path):
        # minio를 위한 S3Hook 생성. 
        s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
        key = KEY_PREFIX + os.path.basename(local_path)
        # minio의 bucket에 local file을 해당 key로 upload 수행. 
        s3_hook.load_file(filename=local_path, key=key, bucket_name=BUCKET_NAME, replace=True)

        #key명 반환
        return key
    
    # upload_to_s3_task = upload_to_s3(local_file_path)
    # local_file_path >> upload_to_s3_task
    
    # upload_to_s3() 인자로 local_file_path를 입력하여 dependency 설정. 
    upload_to_s3(local_file_path)
    

        

