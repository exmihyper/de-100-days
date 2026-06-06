import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="de_db",
    user="de_user",
    password="de_pass"
)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM users;")
count_before = cur.fetchone()[0]
print(f"Пользователей до транзакции: {count_before}")

try:
    print("\nВыполняем транзакцию...")
    
    # Первая вставка — нормальная
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s);",
        ("Рабочий Пользователь", "working@mail.ru")
    )
    print("1. Пользователь вставлен")
    
    # Вторая вставка — ОШИБКА: email 'anna@mail.ru' уже существует (UNIQUE)
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s);",
        ("Ошибочный Пользователь", "anna@mail.ru")
    )
    print("2. Пользователь вставлен")
    
    conn.commit()
    print("Транзакция ЗАФИКСИРОВАНА")

except Exception as e:
    conn.rollback()
    print(f"ОШИБКА: {e}")
    print("Транзакция ОТКАТАНА — ни одна вставка не сохранилась!")

cur.execute("SELECT COUNT(*) FROM users;")
count_after = cur.fetchone()[0]
print(f"\nПользователей после: {count_after}")
print(f"Добавлено: {count_after - count_before} (должен быть 0 — rollback отменил всё)")

cur.close()
conn.close()