-- День 11: Оконные функции
-- 1. ROW_NUMBER: нумерация строк по зарплате
SELECT ROW_NUMBER() OVER (
        ORDER BY salary DESC
    ) AS row_num,
    name,
    department,
    salary
FROM employees;
-- 2. PARTITION BY: нумерация внутри отделов
SELECT ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS row_num,
    name,
    department,
    salary
FROM employees;
-- 3. RANK vs DENSE_RANK
SELECT RANK() OVER (
        ORDER BY salary DESC
    ) AS rank,
    DENSE_RANK() OVER (
        ORDER BY salary DESC
    ) AS dense_rank,
    name,
    salary
FROM employees;
-- 4. LAG и LEAD
SELECT name,
    salary,
    LAG(salary) OVER (
        ORDER BY salary DESC
    ) AS previous_salary,
    LEAD(salary) OVER (
        ORDER BY salary DESC
    ) AS next_salary
FROM employees;
-- Задача 1: Топ-3 по зарплате
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
-- Задача 2: Отклонение от средней по отделу
SELECT name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg,
    salary - AVG(salary) OVER (PARTITION BY department) AS diff_from_avg
FROM employees
ORDER BY department,
    salary DESC;
-- Задача 3: Самый дорогой заказ
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