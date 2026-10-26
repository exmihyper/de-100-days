# День 46: Итоговый проект Недели 7

## Что сделано в Databricks

1. **Загрузка данных** — CSV → Delta-таблица `learning.practice.sales`
2. **SQL-анализ** — топ клиентов с `HAVING SUM(price * quantity) > 10000`
3. **UPDATE** — изменил цену Мыши с 3000 на 4000
4. **Time Travel** — `DESCRIBE HISTORY` показал 2 версии (создание и UPDATE)
5. **VERSION AS OF 0** — прочитал данные до UPDATE (цена Мыши 3000)
6. **Визуализация** — Bar chart выручки по товарам

## Результаты

**Топ клиентов (SQL):**
| user_email | total_spent | orders_count |
|------------|-------------|--------------|
| anna@mail.ru | 130000 | 2 |

**История версий:** 2 (создание, UPDATE)

**Time Travel:** `VERSION AS OF 0` показывает цену Мыши 3000, текущая — 4000.

**График:** Ноутбук — лидер по выручке, Смартфон — второй.

## Итоги Недели 7

| День | Тема | Ключевой навык |
|------|------|-----------------|
| 40 | Знакомство с Databricks | Serverless compute, ноутбуки, загрузка CSV |
| 41 | Spark DataFrame API | `select`, `filter`, `withColumn`, ленивость |
| 42 | Spark SQL | `%sql`, `createOrReplaceTempView`, JOIN |
| 43 | Delta Lake | ACID, `MERGE`, Time Travel, `OPTIMIZE` |
| 44 | Unity Catalog | `catalog.schema.table`, managed tables |
| 45 | Lakeflow | Декларативные пайплайны |
| 46 | Итоговый проект | Полный цикл анализа в Databricks |

## Что освоил
- Работа с облачным Spark
- Spark SQL и DataFrame API
- Delta Lake: ACID, MERGE, Time Travel
- Unity Catalog: структура данных
- Визуализация в ноутбуках Databricks