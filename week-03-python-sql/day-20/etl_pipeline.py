import csv
import logging
import psycopg2
import os


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='etl.log',
    filemode='a',
    encoding='utf-8'
)


console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.getLogger('').addHandler(console)


logger = logging.getLogger(__name__)



def extract(filename):
    logger.info(f"Начало Extract: читаю файл '{filename}'")
    
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            headers = next(reader)
            rows = list(reader)
        
        logger.info(f"Extract завершён: прочитано {len(rows)} строк")
        logger.debug(f"Заголовки CSV: {headers}")
        return rows
    
    except FileNotFoundError:
        logger.error(f"Файл '{filename}' не найден!")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        return []



def transform(rows, cur):
    logger.info(f"Начало Transform: обрабатываю {len(rows)} строк")
    
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
    
    logger.debug(f"Сгруппировано по {len(orders_by_user)} пользователям")
    
    orders = []
    skipped = 0
    
    for email, items in orders_by_user.items():
        cur.execute("SELECT id FROM users WHERE email = %s;", (email,))
        user_row = cur.fetchone()
        
        if user_row is None:
            logger.warning(f"Пропущен пользователь '{email}': не найден в БД")
            skipped += len(items)
            continue
        
        user_id = user_row[0]
        valid_items = []
        
        for item in items:
            cur.execute("SELECT id FROM products WHERE name = %s;", (item['product_name'],))
            product_row = cur.fetchone()
            
            if product_row is None:
                logger.warning(f"Пропущен товар '{item['product_name']}': не найден в БД")
                skipped += 1
                continue
            
            valid_items.append({
                'product_id': product_row[0],
                'quantity': item['quantity'],
                'price': item['price']
            })
        
        if not valid_items:
            continue
        
        total = sum(item['quantity'] * item['price'] for item in valid_items)
        orders.append({
            'user_id': user_id,
            'total_amount': total,
            'items': valid_items
        })
    
    logger.info(f"Transform завершён: сформировано {len(orders)} заказов, пропущено {skipped} позиций")
    return orders

        

def load(orders, cur, conn):
    logger.info(f"Начало Load: вставляю {len(orders)} заказов")
    
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
            logger.debug(f"Вставлен заказ id={order_id}, позиций: {len(order['items'])}")
        
        conn.commit()
        logger.info(f"Load завершён: вставлено {inserted_orders} заказов, {inserted_items} позиций")
    
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при загрузке: {e}")
        logger.error("Транзакция откатана, ничего не вставлено")
        

def main():
    logger.info("=" * 60)
    logger.info("ЗАПУСК ETL-ПАЙПЛАЙНА")
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            database=os.getenv("DB_NAME", "de_db"),
            user=os.getenv("DB_USER", "de_user"),
            password=os.getenv("DB_PASS", "de_pass")
)
        logger.info("Подключение к PostgreSQL установлено")
    except Exception as e:
        logger.critical(f"Не удалось подключиться к БД: {e}")
        return
    
    cur = conn.cursor()
    
    rows = extract('sales_data.csv')
    if not rows:
        logger.warning("Нет данных для обработки. Выход.")
        cur.close()
        conn.close()
        return
    
    orders = transform(rows, cur)
    if not orders:
        logger.warning("Нет валидных заказов. Выход.")
        cur.close()
        conn.close()
        return
    
    load(orders, cur, conn)
    
    cur.execute("SELECT COUNT(*) FROM orders;")
    total_orders = cur.fetchone()[0]
    logger.info(f"Всего заказов в БД: {total_orders}")
    
    cur.close()
    conn.close()
    logger.info("ETL-ПАЙПЛАЙН ЗАВЕРШЁН УСПЕШНО")
    logger.info("=" * 60)



if __name__ == "__main__":
    main()