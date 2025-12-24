from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime

with DAG(
    dag_id="sql_operator_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    # sql인자는 수행할 sql문, 또는 sql이 있는 file명을 기재
    # sql문을 직접 기술할 때는 docstring이 편리
    # 여러개의 sql을 한꺼번에 기술해도 무방
    # auto_commit인자는 default가 False임. 하지만 이는 sql 수행 시 manual 로 commit을 반드시 해야 한다는 의미가 아님. 
    # SQLExecuteQueryOperator는 task가 수행 완료 시에 자동으로 commit을 수행함. 따라서 별도의 commit 문장이 필요 없음. 
    # auto_commit가 True이면 여러 SQL을 수행 시 개별 SQL 수행 시마다 commit을 적용하겠다는 의미임. 
    # 하지만 이런 방식 보다면 필요하다면 여러 SQL 사이에 직접 commit 을 기술하는 것이 더 바람직
    create_table_op = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="mysql_sample_01",
        sql="""
        CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
        );
        """ 
    )

    insert_user_op = SQLExecuteQueryOperator(
        task_id="insert_users",
        conn_id="mysql_sample_01",
        sql="""
        INSERT INTO users (name, age) VALUES
        ('Alice', 30),
        ('Bob', 25),
        ('Charlie', 40);
        """
    )

    create_table_op >> insert_user_op