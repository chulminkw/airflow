from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from pendulum import datetime

def push_value():
    value = "Hello from Task A"
    return value  # auto XCom push!

def pull_value(ti):
    pulled = ti.xcom_pull(task_ids='task_push') # task_ids로 value를 return한 task의 id를 입력받음
    print(f"#### pulled from Xcom {pulled}")

with DAG(
    dag_id="xcom_01",
    start_date=datetime(2025, 12, 2),
    schedule=None,
    catchup=False
) as dag:
    task_push = PythonOperator(
        task_id='task_push',
        python_callable=push_value,
    )

    task_pull = PythonOperator(
        task_id='task_pull',
        python_callable=pull_value,
    )

    task_push >> task_pull