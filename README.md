# apache_airflow

Apache Airflow work in the concept of DAG(Directed Acylic Graph):

Understanding Directed Acyclic Graphs (DAGs) in Apache Airflow
In Apache Airflow, a Directed Acyclic Graph (DAG) is a collection of tasks with defined relationships and dependencies between them. These tasks are represented as nodes in the graph, and the dependencies between tasks are represented as edges.

Here are some key characteristics of DAGs in Apache Airflow:
- Directed: The edges in a DAG have a specific direction, indicating the flow of data or control from one task to another. Tasks can depend on the successful completion of other tasks before they can be executed.

- Acyclic: DAGs do not contain cycles, which means there are no circular dependencies among tasks. This ensures that tasks are executed in a specific order without causing infinite loops or deadlock situations.

- Tasks: Each node in a DAG represents a task, which is a unit of work that needs to be executed. Tasks can be of different types (e.g., BashOperator, PythonOperator, etc.) and perform various actions as part of a workflow.

- Dependencies: Tasks in a DAG can have dependencies on other tasks, specifying the order in which tasks should be executed. Dependencies define the execution flow within the DAG and ensure that tasks are executed in a coordinated manner.

- Schedule: A DAG can be scheduled to run at specific intervals (e.g., daily, hourly) using cron-like expressions. The scheduler in Apache Airflow orchestrates the execution of tasks based on the defined schedule and dependencies.

- Metadata: DAGs in Apache Airflow also store metadata related to tasks, such as task parameters, default arguments, owner information, and more. This metadata helps in managing and monitoring workflows effectively.

Overall, DAGs play a crucial role in defining and visualizing complex workflows in Apache Airflow. By organizing tasks into a directed acyclic structure with explicit dependencies, DAGs enable users to create robust data pipelines and automate data processing tasks efficiently.


### Installation
Install Apache Airflow by this tutorial
```
https://airflow.apache.org/docs/apache-airflow/stable/start.html
```

You can set up your own account by run this command in the terminal 
```
airflow db migrate

airflow users create \
    --username tkdang \
    --firstname Trung Kien \
    --lastname DANG \
    --role Admin \
    --password 123456 \
    --email tkdang@assystem.com

airflow webserver --port 8080

airflow scheduler
```


### Monitering and alerting

Airflow enable you to have fine-grained control over how you monitor your MLops operations and how Airflow alerts you if something goes wrong.

Monitoring:
- Airflow UI: Airflow provides a web-based user interface where you can monitor the status of your DAGs (Directed Acyclic Graphs), tasks, and overall workflow.
- Logging: Utilize logging within your Python operators to log important information, warnings, and errors. You can check the logs to troubleshoot any issues that may arise during the workflow execution.
- Integration with Monitoring Tools: Integrate Airflow with monitoring tools like Prometheus, Grafana, or DataDog for more advanced monitoring capabilities such as tracking performance metrics, resource utilization, and task statuses.

Alerting:
- Email Alerts: Configure email alerts in Airflow to be notified when a task fails or when a DAG encounters an issue. You can set up SMTP settings in the Airflow configuration to send emails.
- Slack Alerts: Integrate Airflow with Slack to receive real-time notifications and alerts directly in your Slack channels. This can help in quickly identifying and resolving any issues.
- Custom Alerts: Use Airflow's on_failure_callback and on_retry_callback parameters in your DAG definition to trigger custom actions, such as sending alerts to external systems or services via APIs

##### Scenario

You can effectively track the performance and health of your machine learning pipelines, enabling you to make informed decisions and quickly address any issues that may arise during execution.

Example :
if we want to build pipeline to preprocessing data like this :
- Convert image to text
- From text convert to huggingface data

If we process a huge amount of images, there will be some cases where things goes wrong, and we will not actually know when your script goes wrong until you run and wait the result. Put try/catch greedly in this case does not help because you don't know how much data you will loss.

In this case, Airflow UI can help you visualize which tasks goes wrong, and logging will help you track the error. Alerting will send you a notification when you are spending time to work on something else and come back to fix the issuse. Further more, since it's API, you can track your workflow anywhere any anytime.

##### Implementation

For the illustration, we will make a demo with by building pipeline to preprocessing data like in MS2-classification of E-cataloging




