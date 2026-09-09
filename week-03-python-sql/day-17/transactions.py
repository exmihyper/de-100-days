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
    
    
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s);",
        ("Рабочий Пользователь", "working@mail.ru")
    )
    print("1. Пользователь вставлен")
    
    
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s);",
        ("Ошибочный Пользователь", "anna@mail.ru")
    )
    print("2. Пользователь вставлен")
    
    
    conn.commit()
    print("Транзакция ЗАФИКСИРОВАНА (commit)")


except Exception as e:
    conn.rollback()
    print(f"ОШИБКА: {e}")
    print("Транзакция ОТКАТАНА (rollback)")
    

cur.execute("SELECT COUNT(*) FROM users;")
count_after = cur.fetchone()[0]
print(f"\nПользователей после транзакции: {count_after}")
print(f"Добавлено: {count_after - count_before}")


cur.execute("SELECT name, email FROM users ORDER BY id DESC LIMIT 3;")
print("\nПоследние пользователи:")
for row in cur.fetchall():
    print(f"  {row[0]} — {row[1]}")

cur.close()
conn.close()