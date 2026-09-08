import csv
import psycopg2


with open('new_products.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    headers = next(reader)  
    rows = list(reader)
    

print(f"Прочитано строк из CSV: {len(rows)}")


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="de_db",
    user="de_user",
    password="de_pass"
)


cur = conn.cursor()


inserted = 0
for row in rows:
    cur.execute("""
        INSERT INTO products (name, description, price, category_id, stock)
        VALUES (%s, %s, %s, %s, %s);
    """, row)
    inserted += 1


conn.commit()


print(f"Вставлено строк: {inserted}")


cur.execute("SELECT COUNT(*) FROM products;")
count = cur.fetchone()[0]
print(f"Всего товаров в таблице: {count}")

cur.close()
conn.close()