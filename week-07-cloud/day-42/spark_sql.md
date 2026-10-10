# День 42: Spark SQL

## Регистрация DataFrame как view

```python
df.createOrReplaceTempView("sales")
```

Теперь `sales` доступен в SQL, как таблица. Это не физическая таблица — это снимок в памяти.

## SQL в Databricks

**Магия `%sql`:**
```sql
%sql
SELECT * FROM sales WHERE price > 10000
```

**Через Python:**
```python
result = spark.sql("SELECT * FROM sales")
display(result)
```

## Пример с JOIN

```sql
%sql
SELECT 
    u.name,
    u.city,
    SUM(s.price * s.quantity) AS total_spent
FROM sales s
JOIN users u ON s.user_email = u.email
WHERE u.city = 'Москва'
GROUP BY u.name, u.city
ORDER BY total_spent DESC
```

Результат:
| name | city | total_spent |
|------|------|-------------|
| Анна | Москва | 130000 |

## Комбинирование DataFrame API и SQL

```python
# SQL возвращает DataFrame
result = spark.sql("SELECT user_email, SUM(price * quantity) AS total FROM sales GROUP BY user_email")

# Регистрируем как view
result.createOrReplaceTempView("summary")

# Работаем с ней дальше
display(spark.sql("SELECT * FROM summary WHERE total > 50000"))
```

## SQL Editor

В Databricks есть отдельный SQL Editor (сайдбар → SQL Editor → New query). Удобно для быстрых запросов без создания ноутбука.

## Что освоил

- `createOrReplaceTempView` — DataFrame как SQL-таблица
- `%sql` в Databricks — чистый SQL в ячейке
- `spark.sql()` — SQL из Python
- JOIN, GROUP BY, WHERE — те же, что в PostgreSQL
- Комбинирование DataFrame API и SQL в одном ноутбуке