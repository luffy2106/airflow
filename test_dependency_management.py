



from airflow import DAG
from airflow.operators.python import PythonVirtualenvOperator
# from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from Depedency_management.task_1.download_data import download_data
from Depedency_management.task_2.preprocess_data import preprocess_data
from Depedency_management.task_3.train_model import train_model
from Depedency_management.task_4.generate_report import generate_report

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

task_1 = PythonVirtualenvOperator(
    task_id='download_data',
    python_callable=download_data,
    requirements=['-r /Depedency_management/task_1/requirements.txt'],
    system_site_packages=False,
    dag=dag,
)

task_2 = PythonVirtualenvOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    requirements=['-r /Depedency_management/task_2/requirements.txt'],
    system_site_packages=False,
    dag=dag,
)

task_3 = PythonVirtualenvOperator(
    task_id='train_model',
    python_callable=train_model,
    requirements=['-r /Depedency_management/task_3/requirements.txt'],
    system_site_packages=False,
    dag=dag,
)

task_4 = PythonVirtualenvOperator(
    task_id='generate_reports',
    python_callable=generate_report,
    requirements=['-r /Depedency_management/task_4/requirements.txt'],
    system_site_packages=False,
    dag=dag,
)

task_1 >> task_2 >> task_3 >> task_4
