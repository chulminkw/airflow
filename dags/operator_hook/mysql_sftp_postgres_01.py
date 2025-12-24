from airflow.sdk import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime

with DAG(
    dag_id="mysql_sftp_postgres_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    select_users_my_op = SQLExecuteQueryOperator(
        task_id="mysql_user_unload",
        conn_id="mysql_sample_01",
        # MySQL DB의 INTO OUTFILE을 이용하여 File로 export 수행
        # OUTFILE 수행 시 DB 권한 및 지정 디렉토리 확인 필요
        # OUTFILE은 overwrite를 하지 않으므로 동일한 파일명 존재 시 오류 발생. 
        # 아래와 같이 template 변수를 이용하여 수행 시마다 파일명 변경
        sql="""
            SELECT *
            FROM users
            INTO OUTFILE '/var/lib/mysql-files/users_{{ ts_nodash }}.csv'
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n';
        """
    )
    
    create_table_pg_op = SQLExecuteQueryOperator(
            task_id="create_table",
            conn_id="postgres_sample_01",
            sql="""
            CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            age INT
            );
            """ 
        )

    select_users_my_op >> create_table_pg_op