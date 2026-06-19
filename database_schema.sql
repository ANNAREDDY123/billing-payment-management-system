CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE customers(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    is_active BOOLEAN
);

CREATE TABLE invoices(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount FLOAT,
    tax FLOAT,
    discount FLOAT,
    total_amount FLOAT,
    due_date DATE,
    status VARCHAR(50)
);

CREATE TABLE invoice_items(
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    product_name VARCHAR(100),
    quantity INTEGER,
    price FLOAT
);

CREATE TABLE payments(
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER UNIQUE,
    amount FLOAT,
    payment_method VARCHAR(50),
    status VARCHAR(50)
);
