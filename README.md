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
    --firstname TrungKien \
    --lastname DANG \
    --role Admin \
    --password 123456 \
    --email tkdang@assystem.com
```

Run the following command in the different terminal

```
airflow webserver --port 8080
```

```
airflow scheduler
```

### Dynamic workflows

In Airflow, dynamic workflows refer to the ability to generate tasks dynamically during runtime based on certain conditions or parameters. This allows for more flexible and customizable workflow orchestration.

#####  Scenario
You can schedule tasks by based on internal trigger or external trigger.
1. Internal trigger

You build a deep learning model but the data keep changing overtime, in this case, you can trigger the model retrained by airflow every month, to update the performance of the model.


2. External trigger 
Sometimes in a workflow, you may have dependencies between tasks in different DAGs. In such cases, you can use a task from an external DAG to trigger a task in the current DAG.

Suppose that you have 2 DAGS like this:
- DAG 1: Download images -> Image processing -> Extract text from image  
- DAG 2: Data transformation -> Data visualization -> train model 


We can see that that the data transformation in DAG 2 should only start after text extraction in DAG 1 has successfully completed. In this case, we can :
- Ensures that the data transformation tasks do not start until the required data is available.
- Maintains the separation of concerns by keeping data extraction and transformation logic in separate DAGs.


##### Implementation

For the illustration, we can use some random dataset online, should choose the data which is not complicated.

Context :
Define tasks for each step in the workflow:
- Task 1: Download data files from an FTP server using a shell script.
- Task 2: Preprocess the data using Python scripts.
- Task 3: Train a machine learning model using a Jupyter notebook or Python script.
- Task 4: Generate reports based on the model predictions.


The pipeline should run one per week, to make sure that we have updated model with updated data all the time. Each task will be excuted if and only if the preceeding task finish.


You can either use :
- If you have only one python file with many fucntions : use ">>" to connect function
- If you have many python files, use Orchestration with BashOperator(BashOperator to execute shell commands/scripts at each step of the workflow)

##### Solution

You can see the demo in the file "work_automation.py". In this example, we make sure
- Each task will be trigged if and only if the previous task sucess
- Whenever a task faied, you got the email notification, you also got the notification when the task is relaunched.
- The failed task will be relaunch maximum one time with time delay of 5 minutes


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


For the illustration, we can use some random dataset online, should choose the data which is not complicated.
Suppose that we have this DAG:
- Task 1: Download data files from an FTP server using a shell script.
- Task 2: Preprocess the data using Python scripts.
- Task 3: Train a machine learning model using a Jupyter notebook or Python script.
- Task 4: Generate reports based on the model predictions.

The pipeline should run one per week, to make sure that we have updated model with updated data all the time. Each task will be excuted if and only if the preceeding task finish.

In this case, Airflow UI can help you visualize which tasks goes wrong, and logging will help you track the error. Alerting will send you a notification when you are spending time to work on something else and come back to fix the issuse. Further more, since it's API, you can track your workflow anywhere any anytime.

##### Implementation
1. If you don't use docker
You can see the implementation in file "work_automation.py". Copy this file into DAG folder in airflow path that you installed(type "airflow info" to check)


Run the following command in the different terminal

```
airflow webserver --port 8080
```

```
airflow scheduler
```

Find the corresponding DAG, you can track the state of running DAG here.

2. If you use docker(recommend)

Use docker help us seperate airflow config in each project, take a look at the tutorial here
```
https://airflow.apache.org/docs/apache-airflow/stable/tutorial/pipeline.html
```


### Dependency management

In practice, solving conflict of virtualenvironment sometimes complicated, becasue each framework require different dependency. Thanks to airflow, you can apply virtualenv created dynamically for each task

you may need to apply dynamic virtual environments for tasks when:
- Different tasks have conflicting dependencies that require specific package versions.
- Tasks need to run in isolation with their own dependency environment.
- You want to ensure reproducibility by encapsulating dependencies within each task.

#####  Scenario
Suppose that you have a function in a task using pytorch that require numpy==1.13, then you have another function to preprocess data in another task which requires numpy==1.10. In this case, we need to isolate the virtualenv of each task to avoid the conflict


##### Implementation

For the illustration, we will make a demo with simple tasks like this :

Let's consider a scenario where two tasks in an Airflow DAG require different versions of the "requests" library. We can create separate virtual environments for each task to isolate their dependencies.
- task_1,task_2,task_3,task_4 are defined as separate tasks within the same Airflow DAG.
- Each task uses a different version of the requests library by specifying it in the requirements parameter.
- By setting system_site_packages=False, we ensure that the tasks run in isolated virtual environments.

This setup allows each task to execute with its specific version of the requests library, avoiding conflicts between dependencies.

Take a look at test_dependency_management.py to see the implementation


### Dynamic workflows

In Airflow, dynamic workflows refer to the ability to generate tasks dynamically during runtime based on certain conditions or parameters. This allows for more flexible and customizable workflow orchestration.

#####  Scenario
You can schedule tasks based on external trigger. For example :
- External trigger : You can define external triggers that determine whether a task should be executed based on the outcome of a previous task or an external condition. Such as when you have new annotation data coming, you can trigger to train model whenever we detect data dift in the current dataset, in this case the behaviour of the model should be updated.

##### Implementation

Take a look at file dinamic_workflows.py to see the implementation. In this implementation, we have 2 DAGS:
- The first DAG download data, preprocess data, and detec data drift, this DAG run weekly
- the second DAG take the data from the first DAG, train the model and generate the report, this DAG run if and only if the result of data drift task of the first DAG is True.

In the UI of airflow, you need to manually activate the first DAG. 


### Extensibility and integration
- Apache Airflow provides its own REST API that allows users to interact with the Airflow system
- Airflow provides a wide range of built-in operators that facilitate integration with different systems such as databases (MySQL, PostgreSQL), cloud services (AWS, GCP), messaging queues (Kafka, RabbitMQ), and more. These operators enable tasks to interact with external resources during workflow execution.
- Hooks in Airflow serve as connectors to external systems by providing a uniform interface to interact with different services. By using hooks, users can easily integrate custom or third-party systems into their Airflow workflows without writing extensive code.

##### Scenario
This is just to show that we can use built-in lib of airflow to interact with other service
- We import the necessary modules from Airflow, including DAG and AWSAthenaOperator.
- Default arguments for the DAG are specified, such as the owner, start date, and retry settings.
- A DAG named 'aws_athena_operator_example' is defined with a daily schedule interval.
- A task (athena_task) is created using AWSAthenaOperator to run a SQL query on Amazon Athena.
- The SQL query to be executed, database name, S3 output location for query results, and AWS connection ID are configured within the operator.
- Task dependencies are set, with no downstream tasks in this simplified example.

##### Implementation

Same as above. Take a look at the script extensibility.py. The example just to show that airflow provide built-in to interact to third party service with mininal code, in this case is AWS.


### Scalability and fault tolerance

Scalability in Apache Airflow refers to the ability of the system to handle increasing workloads by efficiently distributing tasks across multiple worker nodes. Airflow provides horizontal scalability through its distributed architecture, enabling users to scale out their workflow execution as needed.

Key points related to scalability in Airflow include:
- Executor Types: Airflow supports different executor types such as Celery, Dask, Kubernetes, and more, allowing users to choose an executor that best suits their scalability requirements.
- Parallel Execution: Tasks within a DAG can be executed in parallel on multiple worker nodes, enabling faster processing of workflows.
- Task Queues: Airflow uses task queues to distribute tasks among workers, ensuring efficient utilization of resources and optimal performance.
- Cluster Configuration: Users can configure Airflow to run on a cluster of machines, allocating resources dynamically based on workload demands.

Fault Tolerance:
Fault tolerance in Apache Airflow refers to the system's ability to recover from failures or errors without impacting the overall execution of workflows. Airflow provides mechanisms to handle failures gracefully and ensure the reliability of workflow execution.

Key aspects of fault tolerance in Airflow include:
- Task Retries: Users can define the number of retries for each task in a DAG, enabling automatic retry of failed tasks to mitigate transient issues.
- Retry Delay: Users can specify a delay between task retries, allowing time for potential issues to be resolved before retrying the task.
- Deadlock Handling: Airflow detects and prevents deadlocks by monitoring task dependencies and resource availability, ensuring smooth workflow execution.
- Task Resiliency: Airflow isolates tasks within separate processes, enhancing fault isolation and preventing failures in one task from affecting others.

#####  Scenario

###### Scalability
Imagine you are part of a project E-cataloging. The tools has been experiencing a surge in traffic users, leading to an increase in the volume and complexity of data processing tasks. To handle this growth effectively, you have decided to leverage the scalability features of Apache Airflow.

Context
- Scenario: The tool used by thousands of people for doing cataloging
- Challenge: The current data processing workflows, including calling model to extract data, classify section, extract logo and validate, are becoming bottlenecked due to the high workload.
- Goal: Ensure that the data pipelines can scale out seamlessly to accommodate the increased users during the peak time without compromising performance or reliability.

###### Fault Tolerance

Suppose that you want to extract infor from CV but the answer is not your expectation. You can set up the Task Retries: Users can define the number of retries for the task of giving promt question in a DAG, enabling automatic retry of failed tasks to mitigate transient issues.

##### Implementation

###### Scalability 

In this context we can use the ms2-classification model in E-cataloging but we need to create fake requests. 

This implementation is quite complcated because we need to have knowledge about scalibilty such as Kurbenetes or Celery

###### Fault Tolerance 

Set up the threshold to re-ask question to LLM whenever it gave the unexpected answer.

Take a look at French_vocab_app folder to see the implementation. In this example, I build French-English Flashcard. The input is the vocabularies that I saw in the movies and the output is the flashcards with
- The front is French word and its example to illustrate how to use it
- The back is English word and its translation of the example above.

In this problem, I want the length of each example is not over 20 characaters. Airflow will help me repeately invoke the another response again whenever the condition about length is not satisfied. 

We can track the performance of LLM by the UI based on the number of times LLM does not generate the response which qualified all the conditions.


