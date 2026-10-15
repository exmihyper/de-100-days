# День 43: Delta Lake

## Что такое Delta Lake
Формат хранения поверх облачного хранилища. Даёт ACID-транзакции, версионирование, batch + streaming.

Под капотом: Parquet-файлы + транзакционный лог `_delta_log`.

## Запись и чтение
```python
df.write.format("delta").mode("overwrite").saveAsTable("workspace.default.sales_delta")
df_delta = spark.read.table("workspace.default.sales_delta")
```

## Операции
```sql
UPDATE workspace.default.sales_delta SET price = 85000 WHERE product_name = 'Ноутбук';

MERGE INTO workspace.default.sales_delta AS t
USING updates AS s
ON t.user_email = s.user_email AND t.product_name = s.product_name
WHEN MATCHED THEN UPDATE SET t.quantity = s.quantity
WHEN NOT MATCHED THEN INSERT (user_email, product_name, quantity, price)
VALUES (s.user_email, s.product_name, s.quantity, s.price);
```

## История и Time Travel
```sql
DESCRIBE HISTORY workspace.default.sales_delta;
SELECT * FROM workspace.default.sales_delta VERSION AS OF 0;
SELECT * FROM workspace.default.sales_delta TIMESTAMP AS OF '2026-10-15T10:00:00Z';
```

В моём случае: 14 версий (создание, UPDATE, MERGE, OPTIMIZE, VACUUM).

## Обслуживание
```sql
OPTIMIZE workspace.default.sales_delta;  -- объединить мелкие файлы
VACUUM workspace.default.sales_delta;    -- удалить старые файлы (старше 7 дней)
```

**Важно:** после VACUUM старые версии для Time Travel могут стать недоступны.

## Что освоил
- Запись и чтение Delta-таблиц
- UPDATE, DELETE, MERGE (upsert)
- Time Travel — чтение старых версий
- OPTIMIZE и VACUUM
- DESCRIBE HISTORY — аудит изменений