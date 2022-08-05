import os

from airflow import DAG
from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from google.cloud import storage
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'trips_data_all')

# OUTPUT_FILE = 'green_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'
# OUTPUT_FILE_TEMPLATE_FP = 'green_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="move_gcs_trip_data_to_bq_workflow2",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dcamp'],
) as dag:

    for type_of_vehicle in ['yellow', 'green', 'fhv']:

        gcs_to_gcs_task = GCSToGCSOperator(
            task_id=f'gcs_to_gcs_task_{type_of_vehicle}',
            source_bucket=BUCKET,
            source_object=f'raw/{type_of_vehicle}_tripdata*.parquet',
            destination_bucket=BUCKET,
            destination_object=f'{type_of_vehicle}/',
            move_object=True,
        )

        gcs_to_bq_external_task = BigQueryCreateExternalTableOperator(
            task_id=f"bigquery_external_table_task_{type_of_vehicle}",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"external_{type_of_vehicle}_tripdata",
                },
                "externalDataConfiguration": {
                    "autodetect": True,
                    "sourceFormat": "PARQUET",
                    "sourceUris": [f"gs://{BUCKET}/{type_of_vehicle}/*"],
                },
            },
        )

        CREATE_PARTITION_TABLE_QUERY="""SELECT 1"""


        if type_of_vehicle == 'yellow':

            CREATE_PARTITION_TABLE_QUERY=f"""    
                CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{type_of_vehicle}_tripdata_partitoned
                PARTITION BY DATE(tpep_pickup_datetime) AS
                SELECT * REPLACE(NULL AS airport_fee) FROM {BIGQUERY_DATASET}.external_{type_of_vehicle}_tripdata;
            """
        
        elif type_of_vehicle == 'green':

            CREATE_PARTITION_TABLE_QUERY=f"""    
                CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{type_of_vehicle}_tripdata_partitoned
                PARTITION BY DATE(lpep_pickup_datetime) AS
                SELECT * REPLACE(NULL AS ehail_fee) FROM {BIGQUERY_DATASET}.external_{type_of_vehicle}_tripdata;
            """

        elif type_of_vehicle == 'fhv':            

            CREATE_PARTITION_TABLE_QUERY=f"""    
                CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{type_of_vehicle}_tripdata_partitoned
                PARTITION BY DATE(pickup_datetime) AS
                SELECT * REPLACE(NULL AS SR_Flag, NULL AS PUlocationID, NULL AS DOlocationID) FROM {BIGQUERY_DATASET}.external_{type_of_vehicle}_tripdata;
            """

        bq_external_to_partition_table_task = BigQueryInsertJobOperator(
            task_id=f"insert_query_job_{type_of_vehicle}",
            configuration={
                "query": {
                    "query": CREATE_PARTITION_TABLE_QUERY,
                    "useLegacySql": False,
                }
            },
        )

        gcs_to_gcs_task >> gcs_to_bq_external_task >> bq_external_to_partition_table_task