CREATE TABLE customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  price DECIMAL(7,2) NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  order_date DATE NOT NULL,
  total_amount DECIMAL(7,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE
 
TABLE order_items (
  id INTEGER
 
PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER
 
NOT
 
NULL,
  product_id INTEGER
 
NOT
 
NULL,
  quantity INTEGER
 
NOT
 
NULL,
  price DECIMAL(7,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO customers (name, email, phone_number) VALUES
('Juan Dela Cruz', 'juan.delacruz@example.com', '09123456789'),
('Maria Clara', 'maria.clara@example.com', '09987654321');

INSERT INTO products (name, description, price) VALUES
('T-Shirt', 'Basic white t-shirt', 250.00),
('Pants', 'Comfortable blue jeans', 500.00);

INSERT INTO orders (customer_id, order_date, total_amount) VALUES
(1, '2023-12-06', 400.00),
(2, '2023-12-07', 750.00);

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 250.00),
(2, 2, 1, 500.00),
(2, 1, 1, 250.00);