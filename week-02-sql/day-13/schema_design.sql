-- Запрос 1
-- Все заказы пользователя с именем 'Анна' (заказ id, дата, статус, сумма).
SELECT o.id, o.order_date, o.status, o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.name = 'Анна';



-- Запрос 2
-- Сумма total_amount всех заказов по каждому статусу (GROUP BY status).
SELECT status, SUM(total_amount) AS total
FROM orders
GROUP BY status
ORDER BY total DESC;



-- Запрос 3
-- Топ-3 товаров по количеству продаж (SUM quantity из order_items, JOIN products, ORDER BY DESC, LIMIT 3).
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 3;



-- Запрос 4
-- Категории и количество товаров в каждой (JOIN products с categories, COUNT, GROUP BY).
SELECT c.name, COUNT(p.id) AS product_count
FROM categories c
JOIN products p ON c.id = p.category_id
GROUP BY c.name
ORDER BY product_count DESC;