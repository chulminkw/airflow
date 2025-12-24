from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime

# Print XCom results
def _print_results(ti):
    rows = ti.xcom_pull(task_ids="select_users")
    print("Query results:", rows)

with DAG(
    dag_id="sql_operator_02",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
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
    # SELECT 쿼리는 xcom에서 select 결과를 저장함. 너무 많은 결과를 select 하지 않도록 유의
    select_users_op = SQLExecuteQueryOperator(
        task_id="select_users",
        conn_id="mysql_sample_01",
        sql="""
        SELECT * FROM users;
        """
    )
    # _print_results를 호출하여 xcom에서 select_users task 수행 결과를 출력함
    print_results = PythonOperator(
        task_id="print_results",
        python_callable=_print_results
    )

    create_table_op >> insert_user_op >> select_users_op >> print_results