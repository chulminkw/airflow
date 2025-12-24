from airflow.sdk import DAG, task
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from pendulum import datetime

def print_item(item):
    print(f"Got: {item}")

with DAG(
    dag_id="dynamic_mapping_basic",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    @task
    def extract():
        return ["1.csv", "2.csv", "3.csv"]

    @task
    def process(filename):
        print("Processing:", filename)
    # extract()에서 XCom으로 반환된 여러 인자들을(몇개인지 동적으로 변할수 있음) process()에 적용
    process_dtask = process.expand(filename=extract())

    items = ["apple", "banana", "cherry"]
    # partial에 고정된 operator 인자 입력. expand에 여러개의 동적 인자 입력
    print_dtask = PythonOperator.partial(
        task_id="print_task",
        python_callable=print_item,
    ).expand(op_args=[[item] for item in items])

    [process_dtask, print_dtask]

