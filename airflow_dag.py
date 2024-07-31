
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_stock_prediction',
    default_args=default_args,
    description='A simple DAG to predict stock prices using HMM',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 27),
    catchup=False,
)

def download_recent_data():
    os.system('python3 download_recent_data.py')

def predict_and_plot():
    os.system('python3 predict_and_plot.py')

t1 = PythonOperator(
    task_id='download_recent_data',
    python_callable=download_recent_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='predict_and_plot',
    python_callable=predict_and_plot,
    dag=dag,
)

t1 >> t2
