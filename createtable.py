import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("sales.db")

# Create cursor object
cursor = conn.cursor()

# Define SQL statements to create tables
create_customers_table = """
CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone_number VARCHAR(20) NOT NULL
);
"""

create_products_table = """
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  price DECIMAL(7,2) NOT NULL
);
"""

create_orders_table = """
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  order_date DATE NOT NULL,
  total_amount DECIMAL(7,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
"""

create_order_items_table = """
CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  price DECIMAL(7,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
"""

# Execute the SQL statements to create the tables
cursor.execute(create_customers_table)
cursor.execute(create_products_table)
cursor.execute(create_orders_table)
cursor.execute(create_order_items_table)

# Define SQL statements to insert initial data
insert_customers = [
    ("Juan Dela Cruz", "juan.delacruz@example.com", "09123456789"),
    ("Maria Clara", "maria.clara@example.com", "09987654321"),
    ("Kalvin Leonardo", "kalvin.leonardo@example.com", "0912344568")
]

insert_products = [
    ("T-Shirt", "Basic white t-shirt", 250.00),
    ("Pants", "Comfortable blue jeans", 500.00),
]

insert_orders = [
    (1, "2023-12-06", 400.00),
    (2, "2023-12-07", 750.00),
]

insert_order_items = [
    (1, 1, 2, 250.00),
    (2, 2, 1, 500.00),
    (2, 1, 1, 250.00),
]

# Execute the SQL statements to insert the data
for customer in insert_customers:
    cursor.execute("INSERT INTO customers (name, email, phone_number) VALUES (?, ?, ?)", customer)

for product in insert_products:
    cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", product)

for order in insert_orders:
    cursor.execute("INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)", order)

for item in insert_order_items:
    cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", item)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database 'sales.db' created successfully!")