-- Задача 1
-- Найди сотрудников, чья зарплата выше, чем у всех сотрудников из отдела HR. Используй подзапрос с MAX.
SELECT name
FROM employees
WHERE salary > (SELECT MAX(salary) FROM employees WHERE department = 'HR');



-- Задача 2
-- Найди сотрудников, которые сделали заказов на сумму выше средней (средняя сумма заказа на сотрудника). Используй CTE.
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



-- Задача 3
-- Выведи отдел с самой высокой средней зарплатой. Используй ORDER BY и LIMIT.
SELECT department, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
ORDER BY AVG(salary) DESC 
LIMIT 1