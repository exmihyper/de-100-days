-- Запрос 1
-- Для каждой категории найди товар, который принёс больше всего денег (SUM(quantity * price_at_order)).
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



-- Запрос 2
-- Выведи ВСЕХ пользователей. Добавь столбец: 'active' — если сделал хотя бы один заказ 'inactive' — если заказов нет.
SELECT 
    u.name,
    CASE 
        WHEN o.id IS NOT NULL THEN 'active'
        ELSE 'inactive'
    END AS status
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;



-- Запрос 3
-- Для каждого статуса посчитай: Количество заказов, Среднюю сумму заказа (AVG(total_amount)), Общую сумму, Только для статусов, где больше одного заказа (HAVING).
SELECT 
    status,
    COUNT(*) AS order_count,
    ROUND(AVG(total_amount), 2) AS avg_amount,
    SUM(total_amount) AS total_amount
FROM orders
GROUP BY status
HAVING COUNT(*) > 1;



-- Запрос 4
-- Выведи товары, у которых stock < 50. Добавь столбец total_sold (SUM quantity из order_items). Если товар не продавался — показать 0.
SELECT 
    p.name,
    p.stock,
    COALESCE(SUM(oi.quantity), 0) AS total_sold
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
WHERE p.stock < 50
GROUP BY p.name, p.stock
ORDER BY p.stock ASC;



-- Запрос 5
-- Посчитай сумму продаж (total_amount) по месяцам. Выведи месяц (в формате YYYY-MM) и сумму. Отсортируй по месяцу.
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(total_amount) AS total_sales
FROM orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;



-- Запрос 6
-- Для каждого заказа выведи: id заказа, Имя покупателя, Список товаров через запятую (в одном столбце), Общую сумму.
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