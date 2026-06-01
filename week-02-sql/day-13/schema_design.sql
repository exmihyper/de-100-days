-- ==========================================
-- День 13: Проектирование схемы данных
-- ==========================================

-- 1. Удаляем таблицы, если они уже есть
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Создаём таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    registered_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) CHECK (price > 0),
    category_id INTEGER REFERENCES categories(id),
    stock INTEGER CHECK (stock >= 0) DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2) DEFAULT 0 CHECK (total_amount >= 0)
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order DECIMAL(10, 2) NOT NULL CHECK (price_at_order > 0)
);

-- 3. Вставляем данные
INSERT INTO users (name, email) VALUES
('Анна', 'anna@mail.ru'),
('Борис', 'boris@mail.ru'),
('Виктор', 'viktor@mail.ru'),
('Галина', 'galina@mail.ru'),
('Дмитрий', 'dmitry@mail.ru');

INSERT INTO categories (name) VALUES
('Электроника'),
('Одежда'),
('Книги'),
('Спорт');

INSERT INTO products (name, description, price, category_id, stock) VALUES
('Ноутбук', 'Мощный ноутбук для работы', 80000.00, 1, 15),
('Смартфон', 'Современный смартфон', 50000.00, 1, 30),
('Футболка', 'Хлопковая футболка', 1500.00, 2, 100),
('Джинсы', 'Классические джинсы', 4000.00, 2, 50),
('SQL для начинающих', 'Учебник по SQL', 1200.00, 3, 200),
('Python для профи', 'Продвинутый Python', 2500.00, 3, 150),
('Гантели 10 кг', 'Пара гантелей', 3000.00, 4, 40),
('Коврик для йоги', 'Нескользящий коврик', 2000.00, 4, 60);

INSERT INTO orders (user_id, order_date, status, total_amount) VALUES
(1, '2025-01-10', 'delivered', 130000.00),
(2, '2025-01-15', 'processing', 42000.00),
(3, '2025-01-20', 'new', 5000.00);

INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES
(1, 1, 1, 80000.00),
(1, 2, 1, 50000.00),
(2, 4, 2, 4000.00),
(2, 7, 1, 3000.00),
(2, 3, 1, 1500.00),
(3, 5, 2, 1200.00),
(3, 6, 1, 2500.00);

-- 4. SELECT-запросы

-- Запрос 1: Все заказы пользователя 'Анна'
SELECT o.id, o.order_date, o.status, o.total_amount
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.name = 'Анна';

-- Запрос 2: Сумма заказов по статусам
SELECT status, SUM(total_amount) AS total
FROM orders
GROUP BY status
ORDER BY total DESC;

-- Запрос 3: Топ-3 товаров по количеству продаж
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 3;

-- Запрос 4: Категории и количество товаров в каждой
SELECT c.name, COUNT(p.id) AS product_count
FROM categories c
JOIN products p ON c.id = p.category_id
GROUP BY c.name
ORDER BY product_count DESC;