-- Задача 1
-- Выведи имена сотрудников и общую сумму их заказов. Только тех, у кого сумма больше 50000.
SELECT e.name, SUM(o.amount) AS total_sales
FROM employees e
INNER JOIN orders o ON e.id = o.employee_id
GROUP BY e.name
HAVING SUM(o.amount) > 50000;



-- Задача 2
-- Выведи отделы и среднюю сумму заказа по каждому отделу. Используй JOIN сотрудников с заказами.
SELECT e.department, AVG(o.amount) AS avg_sales
FROM employees e
INNER JOIN orders o ON e.id = o.employee_id
GROUP BY e.department;



-- Задача 3
-- Найди продукт, который принёс больше всего денег суммарно. Выведи только его название и сумму.
SELECT product, SUM(amount) AS total_revenue
FROM orders
GROUP BY product
ORDER BY SUM(amount) DESC 
LIMIT 1;



-- Задача 4
-- Выведи сотрудников, которые НЕ сделали ни одного заказа.
SELECT e.name
FROM employees e
LEFT JOIN orders o ON e.id = o.employee_id
WHERE o.id IS NULL;