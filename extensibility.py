from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.athena import AthenaOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 1
}

with DAG('aws_athena_operator_example', 
         default_args=default_args,
         schedule_interval='@daily') as dag:
    
    athena_task = AthenaOperator(
        task_id='run_query',
        query='SELECT * FROM table_name',
        database='your_database',
        output_location='s3://your_bucket/query_results/',
        aws_conn_id='your_aws_connection'
    )
