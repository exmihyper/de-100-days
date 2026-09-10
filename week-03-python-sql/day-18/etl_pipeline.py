import csv
import psycopg2



def extract(filename):
    with open(filename, 'r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader) 
        rows = list(reader) 

    print(f"[Extract] Прочитано строк из CSV: {len(rows)}")
    return rows



def transform(rows, cur):
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
        cur.execute("SELECT id FROM users WHERE email = %s;", (email,))
        user_row = cur.fetchone()

        if user_row is None:
            print(f"[Transform] Пропущен: пользователь с email '{email}' не найден")
            skipped += len(items)
            continue

        user_id = user_row[0]

        valid_items = []
        for item in items:
            cur.execute("SELECT id, price FROM products WHERE name = %s;", (item['product_name'],))
            product_row = cur.fetchone()

            if product_row is None:
                print(f"[Transform] Пропущен: товар '{item['product_name']}' не найден")
                skipped += 1
                continue

            product_id = product_row[0]
            valid_items.append({
                'product_id': product_id,
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

    print(f"[Transform] Сформировано заказов: {len(orders)}")
    print(f"[Transform] Пропущено позиций: {skipped}")
    return orders



def load(orders, cur, conn):
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
        print(f"[Load] Вставлено заказов: {inserted_orders}")
        print(f"[Load] Вставлено позиций: {inserted_items}")

    except Exception as e:
        conn.rollback()
        print(f"[Load] ОШИБКА: {e}")
        print("[Load] Транзакция откатана. Ничего не вставлено.")



def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="de_db",
        user="de_user",
        password="de_pass"
    )
    cur = conn.cursor()

    rows = extract('sales_data.csv')

    orders = transform(rows, cur)

    load(orders, cur, conn)

    cur.execute("SELECT COUNT(*) FROM orders;")
    print(f"\nВсего заказов в БД: {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM order_items;")
    print(f"Всего позиций в БД: {cur.fetchone()[0]}")

    cur.close()
    conn.close()



if __name__ == "__main__":
    main()