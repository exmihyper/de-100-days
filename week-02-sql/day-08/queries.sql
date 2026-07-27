-- Задача 1
-- Выведи всех сотрудников из отдела Finance с зарплатой больше 100000.
SELECT name
FROM employees
WHERE department = 'Finance' AND salary > 100000;



-- Задача 2
-- Выведи названия продуктов из таблицы orders, у которых amount > 10000.
SELECT DISTINCT product
FROM orders
WHERE amount > 10000;



-- Задача 3
-- Выведи имена и даты найма сотрудников, нанятых раньше 2019 года, отсортированных по дате найма (сначала самые старые).
SELECT name, hire_date
FROM employees
WHERE hire_date < '2019-01-01'
ORDER BY hire_date;



-- Задача 4
-- Посчитай количество строк в таблице orders.
SELECT COUNT(*)
FROM orders;
