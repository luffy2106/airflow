from airflow.providers.http.hooks.http import HttpHook
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def fetch_data():
    http_hook = HttpHook(method='GET', http_conn_id='my_http_connection')
    response = http_hook.run(endpoint='/api/data')
    return response.content

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
}

with DAG('http_hook_example', default_args=default_args, schedule_interval='@daily') as dag:
    task_fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data,
    )
