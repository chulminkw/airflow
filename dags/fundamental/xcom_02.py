from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from pendulum import datetime

def push_multiple(ti):
    ti.xcom_push(key='username', value='airflow_user')
    ti.xcom_push(key='run_status', value='success')
    ti.xcom_push(key='score', value=99)

def pull_multiple(ti):
    user = ti.xcom_pull(task_ids='task_push', key='username')
    status = ti.xcom_pull(task_ids='task_push', key='run_status')
    score = ti.xcom_pull(task_ids='task_push', key='score')

    print(f"### User: {user}, Status: {status}, Score: {score}")

def push_multiple_01(ti):
    data = {
        "username": "airflow_user",
        "run_status": "success",
        "score": 99 
    }
    ti.xcom_push(key='user_info', value=data)
    
def pull_multiple_01(ti):
    user_info = ti.xcom_pull(task_ids='task_push', key='user_info')
    print(f"### User info: {user_info}")

def push_dict():
    return {
        'username': 'airflow_user',
        'run_status': 'success',
        'score': 99
    }

def pull_dict(ti):
    pulled = ti.xcom_pull(task_ids='task_pull')
    print(f"#### Pulled: {pulled}")

with DAG(
    dag_id="xcom_multiple",
    start_date=datetime(2025, 12, 2),
    schedule=None,
    catchup=False
) as dag:
    task_push = PythonOperator(
        task_id='task_push',
        python_callable=push_dict,
    )

    task_pull = PythonOperator(
        task_id='task_pull',
        python_callable=pull_dict,
    )

    task_push >> task_pull