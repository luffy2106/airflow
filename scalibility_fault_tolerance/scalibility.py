from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.executors.kubernetes_executor import KubernetesExecutor
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG('kubernetes_example',
          default_args=default_args,
          description='A simple DAG demonstrating Airflow scalability with Kubernetes',
          schedule_interval='@daily',
        )

start = DummyOperator(task_id='start', retries=3, dag=dag)
end = DummyOperator(task_id='end', retries=3, dag=dag)

task1 = DummyOperator(task_id='task1', retries=3, dag=dag)
task2 = DummyOperator(task_id='task2', retries=3, dag=dag)
task3 = DummyOperator(task_id='task3', retries=3, dag=dag)

start >> [task1, task2, task3] >> end

executor = KubernetesExecutor(namespace='airflow',
                              image='apache/airflow:latest',
                              cmds=['bash', '-c'],
                              arguments=['echo Hello from the KubernetesExecutor!'])

dag.executor = executor
