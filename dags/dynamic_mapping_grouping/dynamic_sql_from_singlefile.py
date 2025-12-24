from airflow.sdk import DAG, task, get_current_context
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pendulum import datetime
import os
import sqlparse # pip install sqlparse 필요

BASE_DIR = "/usr/local/airflow"

with DAG(
    dag_id="dynamic_sql_from_single_file",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    template_searchpath=BASE_DIR
) as dag:
    
    # create table은 dynamic task가 아닌 single task로 수행. 
    run_create_tables = SQLExecuteQueryOperator(
        task_id="run_create_tables",
        conn_id="postgres_conn",
        sql="include/sql/create_nw_tables.sql", # 파일명은 반드시 sql 이 되어야 airflow가 sql 파일로 인식. 
        autocommit=True,
    )

    # 두번째 step은 insert_nw_tables.sql을 개별 sql문장으로 parsing하여 list화
    # 이후에 개별 sql문장을 dynamic task로 수행.
    @task
    def parse_insert_sql():
        with open(os.path.join(BASE_DIR, "include/sql/insert_nw_tables.sql")) as f:
            raw_sql = f.read()
        # 빈 라인은 제외하고 개별 sql 문장을 list 형태로 담아서 반환.
        return [stmt.strip() for stmt in sqlparse.split(raw_sql) if stmt.strip()]
    
    @task
    def run_insert_sql(sql):
        # 본 task는 재 수행 시 해당 테이블에 pk가 걸려 있으므로 중복으로 오류 발생. 
        postgres_hook = PostgresHook(postgres_conn_id="postgres_conn")
        postgres_hook.run(sql=sql, autocommit=True)

    # 만약 아래와 같이 dependency를 설정하면, run_create_tables -> parse_insert_sql()이 적용되지 않음
    # dynamic mapping은 mapping source와 mapped task만 명확하게 dependency를 설정. 
    # run_create_tables >> run_insert_sql.expand(sql=parse_insert_sql())
    #  run_create_tables -> parse_insert_sql() 를 설정하려면 아래와 같이 
    # sql_list = parse_insert_sql()로 sql_list가 XComArg로 명확히 설정
    sql_list = parse_insert_sql()
    run_create_tables >> sql_list >> run_insert_sql.expand(sql=sql_list)
    
     
