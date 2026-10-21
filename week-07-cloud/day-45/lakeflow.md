# День 45: Lakeflow — оркестрация в Databricks

## Что такое Lakeflow
Декларативный оркестратор пайплайнов в Databricks. Аналог Airflow, но встроенный в платформу.

## Декларативный vs Императивный
- **Airflow (императивный):** описываешь *как* делать. Задачи, зависимости (`>>`), порядок.
- **Lakeflow (декларативный):** описываешь *что* должно быть. Платформа сама строит граф зависимостей.

## Пример пайплайна (Python)

```python
import dlt

@dlt.table(name="top_customers")
def top_customers():
    return spark.sql("""
        SELECT user_email, SUM(price * quantity) AS total_spent
        FROM learning.practice.sales
        GROUP BY user_email
    """)
```

**Важно:** код с `import dlt` работает только внутри самого пайплайна (через кнопку **Run pipeline** / **Start**), а не в обычном ноутбуке. В обычном ноутбуке будет ошибка `ModuleNotFoundError: No module named 'dlt'`.

## Data Quality (Expectations)

```sql
CREATE OR REFRESH MATERIALIZED VIEW clean_sales (
    CONSTRAINT valid_price EXPECT (price > 0) ON VIOLATION DROP ROW,
    CONSTRAINT valid_quantity EXPECT (quantity > 0) ON VIOLATION DROP ROW
) AS
SELECT * FROM learning.practice.sales;
```

- `EXPECT (условие)` — проверка качества
- `ON VIOLATION DROP ROW` — если условие нарушено, строка удаляется

## Ключевой вывод
В Airflow ты строишь граф руками. В Lakeflow граф строится автоматически на основе того, какие таблицы читаются и создаются. Это следующий уровень оркестрации.