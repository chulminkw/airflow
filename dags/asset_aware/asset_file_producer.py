from airflow.sdk import Asset, DAG, task
from pendulum import datetime

SIMPLE_ASSET = Asset(name="simple_asset",
                     uri="/usr/local/airflow/include/user_data/simple_asset_file.txt")

with DAG(
    dag_id="asset_file_producer",
    start_date=datetime(2025, 12, 1),
    catchup=False,
    tags=["asset_aware"]
) as dag:
    
    @task(outlets=[SIMPLE_ASSET]) # 반드시 outlets는 []로, Asset을 update하는 task 
    def asset_update():
        print(f"asset has been updated:{SIMPLE_ASSET.uri}")

    asset_update()