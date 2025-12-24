# 아래에서 가져옴
# https://registry.astronomer.io/dags/dynamic_s3_copy_source_dest_pairs/versions/1.0.0 에서 가져 옴

from airflow.sdk import DAG, task
from airflow.providers.amazon.aws.operators.s3 import (
    S3CopyObjectOperator, S3ListOperator 
)
from pendulum import datetime

S3_BUCKET_1 = "sample-bucket-01" # bucket 명에 "_"는 허용하지 않음
S3_BUCKET_2 = "sample-bucket-02"

def create_pairs(key):
    source_dest_pair = {
        "source_bucket_key": f"s3://{S3_BUCKET_1}/{key}",
        "dest_bucket_key": f"s3://{S3_BUCKET_2}/copy-from-{S3_BUCKET_1}_{key}"
    }
    return source_dest_pair

with DAG(
    dag_id="s3_dynamic_copy_01",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False
) as dag:
    
    list_files_task = S3ListOperator(
        task_id="list_files_bucket", aws_conn_id="minio_conn", bucket=S3_BUCKET_1
    )
    
    # 소스 S3_BUCKET_1에 있는 모든 key들을 create_pairs() 함수를 통해 타겟 S3_BUCKET_2의 key로 매핑
    source_dest_pairs = list_files_task.output.map(create_pairs)
    print(f"#### list_files_task output:{list_files_task.output}")
    print(f"#### source_dest_pairs:{source_dest_pairs}")

    # dict 기반의
    S3CopyObjectOperator.partial(
        task_id="copy_files_s3", aws_conn_id="minio_conn"
).expand_kwargs(source_dest_pairs)