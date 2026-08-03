-- Задача 1
-- Выведи топ-3 сотрудников с самой высокой зарплатой. Используй ROW_NUMBER() или RANK() и WHERE с подзапросом.
SELECT *
FROM (
        SELECT name,
            salary,
            RANK() OVER (
                ORDER BY salary DESC
            ) AS rnk
        FROM employees
    ) ranked
WHERE rnk <= 3;
-- Задача 2
-- Для каждого сотрудника выведи разницу между его зарплатой и средней зарплатой по его отделу. Используй AVG() OVER (PARTITION BY department)
SELECT name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg
FROM employees
ORDER BY department,
    salary DESC;
-- Задача 3
-- Найди сотрудника, который сделал самый дорогой заказ. Выведи его имя, название продукта и сумму заказа. Используй ROW_NUMBER() и JOIN.
SELECT name,
    product,
    amount
FROM (
        SELECT e.name,
            o.product,
            o.amount,
            ROW_NUMBER() OVER (
                ORDER BY o.amount DESC
            ) AS rn
        FROM orders o
            JOIN employees e ON o.employee_id = e.id
    ) ranked
WHERE rn = 1;