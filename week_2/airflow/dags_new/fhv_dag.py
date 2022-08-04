import os

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# months_ago=42

# execution_dt_yrs_ago=datetime('{{ execution_date.strftime(\'%Y-%m-%d\') }}').date() 
# execution_dt_yrs_ago=datetime.strptime(str('{{ execution_date.strftime(\'%Y-%m-%d\') }}'),'%Y-%m-%d').date() - relativedelta(months=months_ago)

URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
URL_TEMPLATE = URL_PREFIX + '/fhv_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'
OUTPUT_FILE = 'fhv_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'
OUTPUT_FILE_TEMPLATE_FP = 'fhv_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'

#https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-01.parquet

# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


fhv_workflow = DAG(
    "fhv_dag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2019,1,1),
    end_date=datetime(2019,12,31),
)

with fhv_workflow:

    download_data_task = BashOperator(
        task_id='download_data_task',
        bash_command=f"curl -sSL {URL_TEMPLATE} > {path_to_local_home}/{OUTPUT_FILE_TEMPLATE_FP}"
        # bash_command='echo "{{ execution_date.strftime(\'%Y_%m\') }}" '
        # bash_command=f'echo "{URL_TEMPLATE}<-->{path_to_local_home}/{OUTPUT_FILE_TEMPLATE_FP}"'
    )

    # TODO: Homework - research and try XCOM to communicate output values between 2 tasks/operators
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        # bash_command='echo "{{ execution_date.strftime(\'%Y-%m\') }}"'
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{OUTPUT_FILE}",
            "local_file": f"{path_to_local_home}/{OUTPUT_FILE}",
        },
    )

download_data_task >> local_to_gcs_task