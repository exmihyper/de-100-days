-- Задача 1
-- Создай индекс на столбец amount и сравни скорость поиска WHERE amount > 400000 до и после индекса. Запиши время выполнения.
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE amount > 400000;

CREATE INDEX idx_big_sales_amount ON big_sales(amount);

EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE amount > 400000;



-- Задача 2
-- Создай индекс на столбец sale_date и сравни скорость поиска заказов за последние 30 дней.
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE sale_date > CURRENT_DATE - 30;

CREATE INDEX idx_big_sales_date ON big_sales(sale_date);

EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE sale_date > CURRENT_DATE - 30;



-- Задача 3
-- Посмотри на план этого запроса через EXPLAIN.
EXPLAIN
SELECT region, SUM(amount) 
FROM big_sales 
GROUP BY region;