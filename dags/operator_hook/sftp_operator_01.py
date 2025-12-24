from airflow.sdk import DAG
from airflow.providers.sftp.operators.sftp import SFTPOperator
from pendulum import datetime

LOCAL_FILENAME = "test_daily.txt"
LOCAL_DIR = "/home/astro"
SFTP_REMOTE_PATH = f"/home/sftpuser/data/{LOCAL_FILENAME}"

with DAG(
    dag_id="sftp_operator_01",
    start_date=datetime(2025, 12,4),
    schedule=None,
    catchup=False,
) as dag:
    
    upload_to_sftp = SFTPOperator(
        task_id="upload_to_sftp",
        ssh_conn_id="sftp_conn", # sftp용 airflow connection id
        local_filepath=f"{LOCAL_DIR}/{LOCAL_FILENAME}", # local file path
        remote_filepath=SFTP_REMOTE_PATH, # remote file path
        operation="put", # upload
        create_intermediate_dirs=True,
    )

    upload_to_sftp