-- ==========================================
-- День 12: Индексы и EXPLAIN ANALYZE
-- ==========================================

-- 1. Создание большой таблицы (100 000 строк)
DROP TABLE IF EXISTS big_sales CASCADE;

CREATE TABLE big_sales (
    id SERIAL PRIMARY KEY,
    product VARCHAR(50),
    region VARCHAR(30),
    amount INTEGER,
    sale_date DATE
);

INSERT INTO big_sales (product, region, amount, sale_date)
SELECT 
    (ARRAY['Ноутбук', 'Монитор', 'Мышь', 'Клавиатура', 'Принтер', 'Сервер', 'Флешка', 'Бумага'])[floor(random() * 8 + 1)],
    (ARRAY['Москва', 'СПб', 'Казань', 'Новосибирск', 'Екатеринбург'])[floor(random() * 5 + 1)],
    floor(random() * 500000 + 100)::INTEGER,
    CURRENT_DATE - (random() * 730)::INTEGER
FROM generate_series(1, 100000);

SELECT COUNT(*) FROM big_sales;

-- 2. EXPLAIN без индекса — Seq Scan
EXPLAIN
SELECT * FROM big_sales WHERE region = 'Казань';

-- 3. EXPLAIN ANALYZE — реальное время (Seq Scan)
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE region = 'Казань';

-- 4. Создаём индекс на region
CREATE INDEX idx_big_sales_region ON big_sales(region);

-- 5. После индекса — Index Scan
EXPLAIN
SELECT * FROM big_sales WHERE region = 'Казань';

EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE region = 'Казань';

-- 6. Составной индекс
CREATE INDEX idx_big_sales_product_region ON big_sales(product, region);

EXPLAIN ANALYZE
SELECT * FROM big_sales 
WHERE product = 'Ноутбук' AND region = 'Москва';

-- Задача 1: Индекс на amount
-- До индекса
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE amount > 400000;

CREATE INDEX idx_big_sales_amount ON big_sales(amount);

-- После индекса
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE amount > 400000;

-- Задача 2: Индекс на sale_date
-- До индекса
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE sale_date > CURRENT_DATE - 30;

CREATE INDEX idx_big_sales_date ON big_sales(sale_date);

-- После индекса
EXPLAIN ANALYZE
SELECT * FROM big_sales WHERE sale_date > CURRENT_DATE - 30;

-- Задача 3: GROUP BY — Seq Scan (индекс не помогает)
EXPLAIN
SELECT region, SUM(amount) 
FROM big_sales 
GROUP BY region;