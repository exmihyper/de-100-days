from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


def check_connection():
    hook = PostgresHook(postgres_conn_id='postgres_de')
    
    result = hook.get_first("SELECT 'OK' AS status;")
    print(f"Подключение работает: {result}")


def count_users():
    hook = PostgresHook(postgres_conn_id='postgres_de')
    
    count = hook.get_first("SELECT COUNT(*) FROM users;")[0]
    print(f"Пользователей в базе: {count}")


def top_customers():
    """Топ-3 клиента по сумме заказов."""
    hook = PostgresHook(postgres_conn_id='postgres_de')
    
    
    records = hook.get_records("""
        SELECT u.name, SUM(o.total_amount) AS total
        FROM users u
        JOIN orders o ON u.id = o.user_id
        GROUP BY u.name
        ORDER BY total DESC
        LIMIT 3;
    """)
    
    print("=== ТОП-3 КЛИЕНТА ===")
    for name, total in records:
        print(f"  {name}: {total} руб.")


default_args = {
    'owner': 'turbomurzik',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='postgres_dag',
    description='Работа с PostgreSQL через Airflow',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,  # только вручную
    catchup=False,
    tags=['learning', 'day-36', 'postgres'],
) as dag:

    task_check = PythonOperator(
        task_id='check_connection',
        python_callable=check_connection,
    )

    task_count = PythonOperator(
        task_id='count_users',
        python_callable=count_users,
    )

    task_top = PythonOperator(
        task_id='top_customers',
        python_callable=top_customers,
    )

    task_check >> task_count >> task_top