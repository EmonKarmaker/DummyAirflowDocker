from airflow.decorators import dag, task
from datetime import datetime

@dag(
        schedule_interval=None, # None means the DAG won't be scheduled and you'll have to run it manually but you can put any cron expression here 
        start_date=datetime(2022, 1, 1), 
        catchup=False
    )
def dummy_dag():
    @task()
    def dummy_task():
        print('Hello, World!')

    dummy_task()

dag = dummy_dag()