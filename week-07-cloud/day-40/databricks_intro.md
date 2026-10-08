# День 40: Знакомство с Databricks

## Что такое Databricks Free Edition

Облачная платформа для Data Engineering и Data Science. Включает:
- Serverless Spark (не нужно устанавливать локально)
- Delta Lake (формат данных)
- Unity Catalog (управление данными)
- SQL Warehouse (облачные SQL-запросы)
- Lakeflow (оркестрация, аналог Airflow)

## Интерфейс

- **Workspace** — ноутбуки, папки
- **Catalog** — данные (таблицы, volumes)
- **Compute** — serverless кластер (запускается автоматически)
- **SQL Editor** — SQL-запросы отдельно от ноутбуков

## Первый ноутбук

Shift+Enter — выполнить ячейку.

## Чтение CSV через Spark

```python
path = "/Volumes/workspace/default/test/sales_data.csv"
df = spark.read.csv(path, header=True, inferSchema=True)
display(df)