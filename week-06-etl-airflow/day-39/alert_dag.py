import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator



def send_alert(message):
    log_file = '/opt/airflow/dags/alerts.log'
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {message}\n"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(line)
    
    print(f"АЛЕРТ: {message}")


def on_failure(context):
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    execution_date = context['execution_date']
    exception = context.get('exception', 'неизвестно')
    
    message = f"❌ FAILED: {dag_id}.{task_id} | {execution_date} | {exception}"
    send_alert(message)


def on_success(context):
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    
    message = f"✅ SUCCESS: {dag_id}.{task_id}"
    send_alert(message)


def on_retry(context):
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    try_number = context['task_instance'].try_number
    
    message = f"⚠️ RETRY: {dag_id}.{task_id} (попытка {try_number})"
    send_alert(message)


def good_task():
    print("Задача выполняется нормально")


def bad_task():
    raise ValueError("Что-то сломалось — специально")


default_args = {
    'owner': 'turbomurzik',
    'retries': 2,                          
    'retry_delay': timedelta(seconds=10), 
    'on_failure_callback': on_failure,
    'on_success_callback': on_success,
    'on_retry_callback': on_retry,
}

with DAG(
    dag_id='alert_dag',
    description='Демонстрация уведомлений',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['learning', 'day-39', 'alerts'],
) as dag:

    task_good = PythonOperator(
        task_id='good_task',
        python_callable=good_task,
    )

    task_bad = PythonOperator(
        task_id='bad_task',
        python_callable=bad_task,
    )

    task_good >> task_bad