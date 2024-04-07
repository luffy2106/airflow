from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule
import time
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def count_data():
    # Placeholder function to simulate downloading data and counting records
    num_data_records = 100  # Assuming 100 data records for testing
    return num_data_records

def check_data_threshold(**context):
    num_data_records = context['task_instance'].xcom_pull(task_ids='count_data')
    if num_data_records == 100:
        return 'trigger_second_dag'
    else:
        return 'end'
    
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

def drift_detection():
    condition = True
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    # Code for preprocessing data goes here
    print("drift detection step")
    if condition:
        return True
    else:
        return False
    

def train_model():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    # Code for training the model goes here
    print("Train model step")

def generate_report():
    start_time = time.time()
    
    # Run the function for 5 seconds
    while time.time() - start_time < 5:
        # Your function logic goes here
        pass
    
    # Code for generating reports goes here
    print("Generate reports step")

# DAG 1: Data Download, preprocess and detect drift
with DAG('first_dag', 
         default_args=default_args,
         description='DAG to download data, preprocess data and detect drift',
         schedule_interval='@weekly',
         start_date=datetime(2022, 1, 1),
         catchup=False) as dag1:

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data
    )

    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )


    drift_detection_task = BranchPythonOperator(
        task_id='drift_detection',
        python_callable=drift_detection,
        provide_context=True
    )

    trigger_second_dag = TriggerDagRunOperator(
        task_id='trigger_second_dag',
        trigger_dag_id='second_dag',
        conf={"source_dag_id": 'first_dag'},
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    end_task = EmptyOperator(task_id='end')

    download_data_task >> preprocess_data_task >> drift_detection_task
    drift_detection_task >> [trigger_second_dag, end_task]

# DAG 2: Model Training and Report Generation
with DAG('second_dag',
         default_args=default_args,
         description='DAG to train model and generate report',
         schedule_interval=None,
         start_date=datetime(2022, 1, 1),
         catchup=False) as dag2:

    training_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True
    )

    report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
        provide_context=True
    )

    training_task >> report_task

