import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="de_db",
    user="de_user",
    password="de_pass"
)

cur = conn.cursor()

# Топ-3 пользователей по сумме заказов (таблицы users + orders)
cur.execute("""
    SELECT u.name, SUM(o.total_amount) AS total_spent
    FROM users u
    JOIN orders o ON u.id = o.user_id
    GROUP BY u.name
    ORDER BY total_spent DESC
    LIMIT 3;
""")

rows = cur.fetchall()

print("=== ТОП-3 ПОКУПАТЕЛЕЙ ПО СУММЕ ЗАКАЗОВ ===")
for row in rows:
    print(f"{row[0]}: {row[1]} руб.")

cur.close()
conn.close()