from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import time
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,   
    'start_date': datetime(2024, 6, 4),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_data_pipeline',
    default_args=default_args,
    description='A simple data pipeline',
    schedule_interval=timedelta(weeks=1),  # Run the DAG weekly
)

def download_data():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    # Code for preprocessing data goes here
    print("download data step")



def preprocess_data():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    # Code for preprocessing data goes here
    print("Preprocess data step")

def train_model():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    # Code for training the model goes here
    print("Train model step")

def generate_reports():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    
    # Code for generating reports goes here
    print("Generate reports step")


download_data_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    email="tkdang@assystem.com",
    dag=dag,
)

generate_reports_task = PythonOperator(
    task_id='generate_reports',
    python_callable=generate_reports,
    dag=dag,
)

# Setting up task dependencies
download_data_task >> preprocess_data_task >> train_model_task >> generate_reports_task