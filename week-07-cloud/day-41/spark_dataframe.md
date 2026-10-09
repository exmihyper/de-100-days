# День 41: Spark DataFrame API

## Где работал
Databricks Free Edition, ноутбук `day-41-spark-dataframe`.

## Загрузка данных
```python
path = "/Volumes/workspace/default/test/sales_data.csv"
df = spark.read.csv(path, header=True, inferSchema=True)
display(df)
```

## Трансформации (ленивые)

```python
from pyspark.sql.functions import col, sum, count

df.select("user_email", "product_name")
df.filter(col("price") > 10000)
df.withColumn("total", col("price") * col("quantity"))
df.groupBy("user_email").agg(
    sum("total").alias("total_spent"),
    count("*").alias("orders_count")
)
df.orderBy(col("total_spent").desc())
```

## Действия (запускают вычисления)

```python
display(df)   # красивая таблица
df.show()     # простая таблица
df.count()    # количество строк
df.collect()  # список Row
df.take(5)    # первые 5
```

## Практика — цепочка трансформаций

```python
result = (
    df
    .withColumn("total", col("price") * col("quantity"))
    .filter(col("total") > 10000)
    .groupBy("user_email")
    .agg(
        sum("total").alias("total_spent"),
        count("*").alias("orders_count")
    )
    .orderBy(col("total_spent").desc())
)
display(result)
```

### Результат

| user_email | total_spent | orders_count |
|------------|-------------|--------------|
| anna@mail.ru | 130000 | 2 |

Остальные клиенты отфильтрованы, потому что каждая их строка с `total` меньше 10000.

## Ключевое отличие от Pandas

- **Spark ленивый.** Трансформации не выполняются, пока не вызвано действие.
- Если сделать 5 трансформаций и 1 действие — Spark прочитает данные 1 раз.
- `display()` — действие, возвращает `None`. Нельзя `df2 = df.display()`.

## Что освоил

- `select`, `filter`, `withColumn`, `groupBy().agg()`, `orderBy`
- Разница между трансформациями и действиями
- Цепочка трансформаций в стиле Spark