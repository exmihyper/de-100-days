-- День 9: JOIN — практические задачи
-- Задача 1: Сотрудники с общей суммой заказов > 50000
SELECT e.name,
    SUM(o.amount) AS total_sales
FROM employees e
    JOIN orders o ON e.id = o.employee_id
GROUP BY e.name
HAVING SUM(o.amount) > 50000;
-- Задача 2: Средняя сумма заказа по отделам
SELECT e.department,
    AVG(o.amount) AS avg_order
FROM employees e
    JOIN orders o ON e.id = o.employee_id
GROUP BY e.department;
-- Задача 3: Продукт с наибольшей суммарной выручкой
SELECT o.product,
    SUM(o.amount) AS total_revenue
FROM orders o
GROUP BY o.product
ORDER BY total_revenue DESC
LIMIT 1;
-- Задача 4: Сотрудники без заказов
SELECT e.name
FROM employees e
    LEFT JOIN orders o ON e.id = o.employee_id
WHERE o.id IS NULL;