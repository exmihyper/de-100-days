-- День 10: Подзапросы и CTE

-- 1. Сотрудники с зарплатой выше средней
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 2. Сотрудники, у которых есть заказы (подзапрос с IN)
SELECT name
FROM employees
WHERE id IN (SELECT DISTINCT employee_id FROM orders WHERE employee_id IS NOT NULL);

-- 3. Количество заказов каждого сотрудника (подзапрос в SELECT)
SELECT 
    e.name,
    (SELECT COUNT(*) FROM orders o WHERE o.employee_id = e.id) AS order_count
FROM employees e
ORDER BY order_count DESC;

-- 4. CTE: сотрудники с суммой заказов выше средней
WITH emp_totals AS (
    SELECT employee_id, SUM(amount) AS total
    FROM orders
    WHERE employee_id IS NOT NULL
    GROUP BY employee_id
)
SELECT e.name, et.total
FROM employees e
JOIN emp_totals et ON e.id = et.employee_id
WHERE et.total > (SELECT AVG(total) FROM emp_totals);

-- Задача 1: Зарплата выше всех в HR
SELECT name
FROM employees
WHERE salary > (SELECT MAX(salary) FROM employees WHERE department = 'HR');

-- Задача 2: CTE + сравнение со средним
WITH emp_totals AS (
    SELECT employee_id, SUM(amount) AS total
    FROM orders
    WHERE employee_id IS NOT NULL
    GROUP BY employee_id
)
SELECT e.name, et.total
FROM employees e
JOIN emp_totals et ON e.id = et.employee_id
WHERE et.total > (SELECT AVG(total) FROM emp_totals);

-- Задача 3: Отдел с самой высокой средней зарплатой
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC
LIMIT 1;