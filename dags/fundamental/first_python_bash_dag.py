from airflow.sdk import DAG, chain
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from pendulum import datetime

def print_hello():
    print("#### Hello from PythonOperator!")

with DAG(
    dag_id="first_python_bash_dag",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["example", "tutorial"]
) as dag:
    
    # bash command을 수행하는 task operator로 task로 수행됨
    # Operator는 반드시 task_id를 가짐. 개별 Operator별로 특징적인 argument들을 가짐
    bash_task = BashOperator(
        task_id="print_date_bash",
        bash_command='echo "##### today: `date`"'
    )

    # python function(python 파일이 아님)을 수행하는 task operator
    python_task = PythonOperator(
        task_id="say_hello_python",
        python_callable=print_hello
    )

    # task들의 수행 dependency 설정
    bash_task >> python_task
    #chain(bash_task, python_task)