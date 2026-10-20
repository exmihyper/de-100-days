# День 44: Unity Catalog

## Трёхуровневая структура
```
Catalog (learning)
  └── Schema (practice)
      ├── Table (sales)
      └── Volume (test)
```

Полное имя: `learning.practice.sales`

## Создание
```sql
CREATE CATALOG IF NOT EXISTS learning;
CREATE SCHEMA IF NOT EXISTS learning.practice;
```

## Запись таблицы
```python
df.write.format("delta").mode("overwrite").saveAsTable("learning.practice.sales")
```

## Managed vs External

| | Managed | External |
|---|---|---|
| Кто хранит файлы | Unity Catalog | Ты сам |
| DROP TABLE | Данные удаляются | Данные остаются |
| Рекомендуется для | Новые таблицы | Устаревшие данные |

## Права доступа (для команды)
```sql
GRANT SELECT ON TABLE learning.practice.sales TO `user@example.com`;
GRANT USE CATALOG ON CATALOG learning TO `user@example.com`;
GRANT USE SCHEMA ON SCHEMA learning.practice TO `user@example.com`;
```

**Важно:** в Free Edition один пользователь — GRANT на других не работает. Концепция понятна, практика требует команды.

## Что освоил
- Трёхуровневая структура: catalog.schema.table
- Создание своих каталогов и схем
- Запись managed таблиц
- Концепция прав доступа
- Catalog Explorer — визуальный обзор данных