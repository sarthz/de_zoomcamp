import os

from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingest_script import ingest_callable

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
dataset_file = "yellow_tripdata_2021-01.csv"


PG_HOST=os.getenv('PG_HOST')
PG_USER=os.getenv('PG_USER')
PG_PASSWORD=os.getenv('PG_PASSWORD')
PG_PORT=os.getenv('PG_PORT')
PG_DATABASE=os.getenv('PG_DATABASE')

local_workflow = DAG(
    "LocalIngestionDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2022,1,1)
)


url = f"https://nyc-tlc.s3.amazonaws.com/csv_backup/{dataset_file}"

URL_PREFIX = 'https://nyc-tlc.s3.amazonaws.com/csv_backup'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'

with local_workflow:

    wget_task = BashOperator(
        task_id='wget',
        # bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
        bash_command='echo "{{ execution_date.strftime(\'%Y_%m\') }}" '
    )

    # ingest_task = PythonOperator(
    #     task_id='ingest',
    #     python_callable=ingest_callable,
    #     # python_callable=abc
    #     op_kwargs=dict(
    #         user=PG_USER, 
    #         password=PG_PASSWORD, 
    #         host=PG_HOST, 
    #         port=PG_PORT, 
    #         db=PG_DATABASE, 
    #         table_name=TABLE_NAME_TEMPLATE, 
    #         csv_file=OUTPUT_FILE_TEMPLATE,
    #         URL_TEMPLATE=URL_TEMPLATE
    #     )
    # )

    # wget_task >> ingest_task
    wget_task