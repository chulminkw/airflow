from airflow.sdk import DAG, task, task_group
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pendulum import datetime
import pandas as pd
import requests

"""아래에서 발췌함
https://registry.astronomer.io/dags/astro_cratedb_elt_pipeline/versions/1.0.0
https://github.com/astronomer/astro-cratedb-blogpost/blob/1.0.0/dags/astro_cratedb_elt_pipeline.py
"""
POSTGRES_CONN_ID = "postgres_sample_01"
GH_API_URL = "https://api.github.com/repos/astronomer/learn-tutorials-data"
GH_CONTENT_URL = "https://raw.githubusercontent.com/astronomer/learn-tutorials-data"
GH_FOLDER_PATH = "/possum_partial"

@task
def get_file_names(base_url, folder_path):
    # get the names of all files in a folder in a github repo."
    folder_url = base_url + "/contents" + folder_path
    response = requests.get(folder_url)
    files = response.json()
    file_names = [file["name"] for file in files]
    return file_names

@task
def extract_data(base_url, folder_path, file_name):
    """Extract the contents of a csv file in a github repo and
    return a pandas DataFrame."""
    file_url = base_url + "/main" + folder_path + f"/{file_name}"
    possum_data = pd.read_csv(file_url)
    return possum_data

@task
def transform_data(dataset):
    """Transform the data by dropping rows with missing values 
    Return a tuple of lists of column values """
    possum_final = dataset.dropna()
    return tuple(possum_final.to_dict(orient="list").values())

with DAG(
    dag_id="task_group_01",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["include/"]
) as dag:
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=POSTGRES_CONN_ID,
        sql="sql/create_table_01.sql"
    )

    file_names = get_file_names(base_url=GH_API_URL, folder_path=GH_FOLDER_PATH)
    print(f"##### file_names: {file_names} #####")
    create_table >> file_names

    @task_group
    def extract_to_load(base_url, folder_path, file_name):
        """Extract data from a CSV file in a GitHub repo, 
        transform it and load it into PostgreSQL"""
        
        extracted_data = extract_data(
            base_url=base_url, folder_path=folder_path, file_name=file_name
        )
        
        transformed_data = transform_data(dataset=extracted_data)

        SQLExecuteQueryOperator(
            task_id="load_data",
            conn_id=POSTGRES_CONN_ID,
            sql="sql/insert_data.sql",
            parameters=transformed_data,
        )

    #dynamically map the task group over the list of filenames, 
    #creating one task group for each file
    extract_to_load_tg = extract_to_load.partial(
        base_url=GH_CONTENT_URL, folder_path=GH_FOLDER_PATH
    ).expand(file_name=file_names)