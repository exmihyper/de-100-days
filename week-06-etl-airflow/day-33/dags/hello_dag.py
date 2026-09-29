from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def say_hello():
    """Простая функция — печатает приветствие."""
    print("=" * 50)
    print("Привет из Airflow!")
    print("=" * 50)


def say_goodbye(name):
    """Функция с параметром."""
    print(f"До свидания, {name}!")
    
    
default_args = {
    'owner': 'turbomurzik',           
    'depends_on_past': False,          
    'email_on_failure': False,         
    'email_on_retry': False,
    'retries': 1,                     
    'retry_delay': timedelta(minutes=1) 
}


with DAG(
    dag_id='hello_dag',                
    description='Мой первый DAG',      
    default_args=default_args,
    start_date=datetime(2026, 1, 1),   
    schedule='@daily',        
    catchup=False,                     
    tags=['learning', 'day-34'],       
) as dag:
    
    
    task_bash = BashOperator(
        task_id='print_date',          
        bash_command='date',            
    )

    
    task_hello = PythonOperator(
        task_id='say_hello',
        python_callable=say_hello,      
    )


    task_goodbye = PythonOperator(
        task_id='say_goodbye',
        python_callable=say_goodbye,
        op_kwargs={'name': 'Студент'}, 
    )
    
    
    task_bash >> task_hello >> task_goodbye
