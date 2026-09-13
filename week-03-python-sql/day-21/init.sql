CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    registered_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) CHECK (price > 0),
    category_id INTEGER REFERENCES categories(id),
    stock INTEGER CHECK (stock >= 0) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'new' CHECK (status IN ('new', 'processing', 'shipped', 'delivered', 'cancelled')),
    total_amount DECIMAL(10, 2) DEFAULT 0 CHECK (total_amount >= 0)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_order DECIMAL(10, 2) NOT NULL CHECK (price_at_order > 0)
);

INSERT INTO users (name, email) VALUES
('Анна', 'anna@mail.ru'),
('Борис', 'boris@mail.ru'),
('Виктор', 'viktor@mail.ru'),
('Галина', 'galina@mail.ru'),
('Дмитрий', 'dmitry@mail.ru');

INSERT INTO categories (name) VALUES
('Электроника'), ('Одежда'), ('Книги'), ('Спорт');

INSERT INTO products (name, price, category_id, stock) VALUES
('Ноутбук', 80000.00, 1, 15),
('Смартфон', 50000.00, 1, 30),
('Футболка', 1500.00, 2, 100),
('Джинсы', 4000.00, 2, 50),
('SQL для начинающих', 1200.00, 3, 200),
('Python для профи', 2500.00, 3, 150),
('Гантели 10 кг', 3000.00, 4, 40),
('Коврик для йоги', 2000.00, 4, 60);