import csv
import psycopg2

# 1. Читаем CSV
with open('new_products.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    headers = next(reader)  # Пропускаем заголовки
    rows = list(reader)     # Все строки данных

print(f"Прочитано строк из CSV: {len(rows)}")

# 2. Подключаемся к базе
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="de_db",
    user="de_user",
    password="de_pass"
)
cur = conn.cursor()

# 3. Вставляем данные
inserted = 0
for row in rows:
    # row = ['Наушники', 'Беспроводные наушники', '7000.00', '1', '25']
    cur.execute("""
        INSERT INTO products (name, description, price, category_id, stock)
        VALUES (%s, %s, %s, %s, %s);
    """, row)
    inserted += 1

# 4. Фиксируем изменения (COMMIT)
conn.commit()

print(f"Вставлено строк: {inserted}")

# 5. Проверяем
cur.execute("SELECT COUNT(*) FROM products;")
count = cur.fetchone()[0]
print(f"Всего товаров в таблице: {count}")

cur.close()
conn.close()