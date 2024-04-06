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
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --password your_password_here \
    --email spiderman@superhero.org

airflow webserver --port 8080

airflow scheduler
```


### Dynamic workflows

In Airflow, dynamic workflows refer to the ability to generate tasks dynamically during runtime based on certain conditions or parameters. This allows for more flexible and customizable workflow orchestration.

#####  Scenario

1. Updating model
You can schedule tasks by based on internal trigger or external trigger. For example :
- Internal trigger : You build a deep learning model but the data keep changing overtime, in this case, you can trigger the model retrained by airflow every month, to update the performance of the model.



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
- Whenever a task faied, you got the email notification
- The failed task will be relaunch maximum one time with time delay of 5 minutes



