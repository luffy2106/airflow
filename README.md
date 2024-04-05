# apache_airflow

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
You can schedule tasks by based on internal trigger or external trigger. For example :
- Internal trigger : You build a deep learning model but the data keep changing overtime, in this case, you can trigger the model retrained by airflow every month, to update the performance of the model.
- External trigger : You can define external triggers that determine whether a task should be executed based on the outcome of a previous task or an external condition. Such as when you have new annotation data coming, you can trigger to train model whenever we have more than X data available.

##### Implementation

For the illustration, we can use some random dataset online, should choose the data which is not complicated.

Context :
Define tasks for each step in the workflow:
- Task 1: Download data files from an FTP server using a shell script.
- Task 2: Preprocess the data using Python scripts.
- Task 3: Train a machine learning model using a Jupyter notebook or Python script.
- Task 4: Generate reports based on the model predictions.


The pipeline should run one per week, to make sure that we have updated model with updated data all the time. Each task will be excuted if and only if the preceeding task finish.

