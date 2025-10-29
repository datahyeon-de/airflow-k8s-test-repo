"""
Example DAG for testing Git-Sync with Kubernetes
"""
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'example_bash_dag',
    default_args=default_args,
    description='A simple bash DAG for Git-Sync testing',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'test'],
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = BashOperator(
        task_id='print_env',
        bash_command='env | head -20 && sleep 60',
    )
    
    t3 = BashOperator(
        task_id='wait_time',
        bash_command='sleep 60',
    )

    t1 >> t2 >> t3

