from airflow.sdk import DAG, Asset, dag, task
from pendulum import datetime

# https://www.astronomer.io/docs/learn/airflow-datasets 에서 발췌
with DAG(
    dag_id="simple_asset_producer",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False
) as producer_dag:
    @task(outlets=[Asset("my_asset")])
    def my_producer_task():
        print("##### asset has been updated")

    my_producer_task()

# 2개의 DAG를 한 파일에 기재하는 것은 가득성을 위해 좋은 선택은 아니지만, 실습을 위해 진행
with DAG(
    dag_id="simple_asset_consumer",
    start_date=datetime(2025, 12, 1),
    schedule=[Asset("my_asset")], # my_asset에 종속되어 수행
    catchup=False
) as consumer_dag:

    @task
    def my_consumer_task():
        print("##### consumer task has been executed")

    my_consumer_task()
