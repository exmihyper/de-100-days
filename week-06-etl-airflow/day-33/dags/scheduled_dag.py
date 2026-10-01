from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


def extract():
    print("Extract: забираем данные из источника")


def transform_clean():
    print("Transform 1: очистка данных")


def transform_enrich():
    print("Transform 2: обогащение данных")


def load():
    print("Load: загружаем в базу")


def check_quality():
    data_is_clean = True
    if data_is_clean:
        return 'quality_ok'
    else:
        return 'quality_fail'


def on_quality_ok():
    print("Качество в норме — продолжаем")


def on_quality_fail():
    print("Данные грязные — останавливаемся")


default_args = {
    'owner': 'turbomurzik',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='scheduled_dag',
    description='Расписание и зависимости',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule='0 6 * * *',
    catchup=False,
    tags=['learning', 'day-35'],
) as dag:

    start = EmptyOperator(task_id='start')

    task_extract = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    task_clean = PythonOperator(
        task_id='transform_clean',
        python_callable=transform_clean,
    )

    task_enrich = PythonOperator(
        task_id='transform_enrich',
        python_callable=transform_enrich,
    )

    task_load = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    task_check = BranchPythonOperator(
        task_id='check_quality',
        python_callable=check_quality,
    )

    task_ok = PythonOperator(
        task_id='quality_ok',
        python_callable=on_quality_ok,
    )

    task_fail = PythonOperator(
        task_id='quality_fail',
        python_callable=on_quality_fail,
    )
    
    
    task_extract >> [task_clean, task_enrich] >> task_load >> task_check
    task_check >> [task_ok, task_fail]