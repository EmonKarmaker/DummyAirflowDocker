from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'finn_scrapper_dag',
    default_args=default_args,
    description='Finn Scraper Pipeline',
    schedule_interval='30 14 * * *',  # Runs daily at 2:30 PM
    start_date=datetime(2025, 1, 17),
    catchup=False,
)

# Define task functions
def run_script(script_name):
    """Runs a script from the src folder."""
    subprocess.run(['python', f'/opt/airflow/dags/FinnScrapper/src/{script_name}'], check=True)

# Tasks
fetch_links_task = PythonOperator(
    task_id='fetch_links',
    python_callable=lambda: run_script('fetch_links.py'),
    dag=dag,
)

scrape_details_task = PythonOperator(
    task_id='scrape_details',
    python_callable=lambda: run_script('scrape_details.py'),
    dag=dag,
)

process_ads_task = PythonOperator(
    task_id='process_ads',
    python_callable=lambda: run_script('process_ads.py'),
    dag=dag,
)

check_existing_ads_task = PythonOperator(
    task_id='check_existing_ads',
    python_callable=lambda: run_script('check_existing_ads.py'),
    dag=dag,
)

upload_to_mongo_task = PythonOperator(
    task_id='upload_to_mongo',
    python_callable=lambda: run_script('upload_to_mongo.py'),
    dag=dag,
)

# Task dependencies
fetch_links_task >> scrape_details_task >> process_ads_task >> check_existing_ads_task >> upload_to_mongo_task
