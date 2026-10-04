from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor


def process_file(**context):
    
    import os

    filename = '/opt/airflow/dags/incoming/orders.csv'

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')

        print(f"Файл найден: {filename}")
        print(f"Строк в файле: {len(lines)}")
        print("Содержимое:")
        print(content)
    else:
        print(f"Файл не найден: {filename}")


def archive_file():
    
    import os
    import shutil

    src = '/opt/airflow/dags/incoming/orders.csv'
    dst = '/opt/airflow/dags/archive/orders.csv'

    os.makedirs('/opt/airflow/dags/archive', exist_ok=True)

    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Файл перемещён в {dst}")
    else:
        print("Нет файла для архивации")


default_args = {
    'owner': 'turbomurzik',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='sensor_dag',
    description='Ждём появления файла и обрабатываем',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,  
    catchup=False,
    tags=['learning', 'day-38', 'sensor'],
) as dag:

    
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/opt/airflow/dags/incoming/orders.csv',
        poke_interval=10,
        timeout=120,
        mode='reschedule',
        soft_fail=False,  
    )

    task_process = PythonOperator(
        task_id='process_file',
        python_callable=process_file,
    )

    task_archive = PythonOperator(
        task_id='archive_file',
        python_callable=archive_file,
    )

    wait_for_file >> task_process >> task_archive