SELECT name
FROM employees
WHERE department = 'Finance'
AND salary > 100000
;

SELECT DISTINCT product
FROM orders
WHERE amount > 10000
;

SELECT name, hire_date
FROM employees
WHERE hire_date < '2019-01-01'
ORDER BY hire_date ASC
;

SELECT COUNT(*)
FROM orders
;