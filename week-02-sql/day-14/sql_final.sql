-- ==========================================
-- День 14: Финальный проект Недели SQL
-- ==========================================

-- Запрос 1: Лидеры продаж по категориям
-- Находит товар с максимальной выручкой в каждой категории
WITH ranked AS (
    SELECT 
        c.name AS category,
        p.name AS product,
        SUM(oi.quantity * oi.price_at_order) AS total_revenue,
        ROW_NUMBER() OVER (PARTITION BY c.name ORDER BY SUM(oi.quantity * oi.price_at_order) DESC) AS rn
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    GROUP BY c.name, p.name
)
SELECT category, product, total_revenue
FROM ranked
WHERE rn = 1;

-- Запрос 2: Активные vs неактивные пользователи
SELECT 
    u.name,
    CASE 
        WHEN o.id IS NOT NULL THEN 'active'
        ELSE 'inactive'
    END AS status
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.name, status;

-- Запрос 3: Средний чек по статусам заказов
SELECT 
    status,
    COUNT(*) AS order_count,
    ROUND(AVG(total_amount), 2) AS avg_amount,
    SUM(total_amount) AS total_amount
FROM orders
GROUP BY status
HAVING COUNT(*) > 1;

-- Запрос 4: Товары с низким запасом и их продажи
SELECT 
    p.name,
    p.stock,
    COALESCE(SUM(oi.quantity), 0) AS total_sold
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE p.stock < 50
GROUP BY p.name, p.stock
ORDER BY p.stock ASC;

-- Запрос 5: Месячная динамика продаж
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;

-- Запрос 6: Чеки с детализацией
SELECT 
    o.id AS order_id,
    u.name AS customer,
    STRING_AGG(p.name, ', ' ORDER BY p.name) AS products,
    o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
GROUP BY o.id, u.name, o.total_amount
ORDER BY o.id;