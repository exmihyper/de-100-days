import csv
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook




def extract(**context):
    
    filename = '/opt/airflow/dags/sales_data.csv'
    
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)
        rows = list(reader)
    
    print(f"Прочитано строк: {len(rows)}")
    print(f"Заголовки: {headers}")
    
    
    context['ti'].xcom_push(key='raw_rows', value=rows)




def transform(**context):
    """Проверяет данные и группирует в заказы."""
    rows = context['ti'].xcom_pull(task_ids='extract', key='raw_rows')
    
    if not rows:
        raise ValueError("Нет данных из Extract")
    
    print(f"Получено строк из Extract: {len(rows)}")
    
    
    hook = PostgresHook(postgres_conn_id='postgres_de')
    
   
    orders_by_user = {}
    for row in rows:
        email = row[0]
        product_name = row[1]
        quantity = int(row[2])
        price = float(row[3])
        
        if email not in orders_by_user:
            orders_by_user[email] = []
        orders_by_user[email].append({
            'product_name': product_name,
            'quantity': quantity,
            'price': price
        })
    
    
    orders = []
    skipped = 0
    
    for email, items in orders_by_user.items():
        user_row = hook.get_first(
            "SELECT id FROM users WHERE email = %s;",
            parameters=(email,)
        )
        
        if user_row is None:
            print(f"Пропущен пользователь '{email}': не найден")
            skipped += len(items)
            continue
        
        user_id = user_row[0]
        valid_items = []
        
        for item in items:
            product_row = hook.get_first(
                "SELECT id FROM products WHERE name = %s;",
                parameters=(item['product_name'],)
            )
            
            if product_row is None:
                print(f"Пропущен товар '{item['product_name']}'")
                skipped += 1
                continue
            
            valid_items.append({
                'product_id': product_row[0],
                'quantity': item['quantity'],
                'price': item['price']
            })
        
        if not valid_items:
            continue
        
        total = sum(i['quantity'] * i['price'] for i in valid_items)
        orders.append({
            'user_id': user_id,
            'total_amount': total,
            'items': valid_items
        })
    
    print(f"Сформировано заказов: {len(orders)}, пропущено: {skipped}")
    
    
    context['ti'].xcom_push(key='orders', value=orders)




def load(**context):
    orders = context['ti'].xcom_pull(task_ids='transform', key='orders')
    
    if not orders:
        raise ValueError("Нет заказов для загрузки")
    
    print(f"Загружаю заказов: {len(orders)}")
    
    hook = PostgresHook(postgres_conn_id='postgres_de')
    conn = hook.get_conn()
    cur = conn.cursor()
    
    inserted_orders = 0
    inserted_items = 0
    
    try:
        for order in orders:
            cur.execute(
                "INSERT INTO orders (user_id, total_amount) VALUES (%s, %s) RETURNING id;",
                (order['user_id'], order['total_amount'])
            )
            order_id = cur.fetchone()[0]
            
            for item in order['items']:
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES (%s, %s, %s, %s);",
                    (order_id, item['product_id'], item['quantity'], item['price'])
                )
                inserted_items += 1
            
            inserted_orders += 1
        
        conn.commit()
        print(f"Успешно: {inserted_orders} заказов, {inserted_items} позиций")
    
    except Exception as e:
        conn.rollback()
        print(f"ОШИБКА: {e}. Транзакция откатана.")
        raise
    
    finally:
        cur.close()
        conn.close()




def report(**context):
    
    hook = PostgresHook(postgres_conn_id='postgres_de')
    
    total_orders = hook.get_first("SELECT COUNT(*) FROM orders;")[0]
    total_revenue = hook.get_first("SELECT SUM(total_amount) FROM orders;")[0]
    
    print("=" * 50)
    print("ОТЧЁТ")
    print("=" * 50)
    print(f"Всего заказов в БД: {total_orders}")
    print(f"Общая выручка: {total_revenue} руб.")
    
    top = hook.get_records("""
        SELECT u.name, SUM(o.total_amount) AS total
        FROM users u
        JOIN orders o ON u.id = o.user_id
        GROUP BY u.name
        ORDER BY total DESC
        LIMIT 3;
    """)
    
    print("\nТоп-3 клиента:")
    for name, total in top:
        print(f"  {name}: {total} руб.")




default_args = {
    'owner': 'turbomurzik',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='etl_dag',
    description='ETL из CSV в PostgreSQL через Airflow',
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['learning', 'day-37', 'etl'],
) as dag:

    task_extract = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )

    task_transform = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )

    task_load = PythonOperator(
        task_id='load',
        python_callable=load,
    )

    task_report = PythonOperator(
        task_id='report',
        python_callable=report,
    )

    task_extract >> task_transform >> task_load >> task_report