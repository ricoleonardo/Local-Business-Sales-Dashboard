import sqlite3
import pandas as pd


# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("pinoybiz_sales1.db")

# Create cursor object
cursor = conn.cursor()

# 3. Dashboard Queries:

#cursor.execute("""
#SELECT
#  o.customer_id,
#  o.product,
#  CAST(o.amount AS DECIMAL(7,2)) AS amount,
#  c.name,
#  o.order_date,
#  SUM(CAST(o.amount AS DECIMAL(7,2))) AS total_amount
#FROM orders o
#INNER JOIN customers c ON o.customer_id = c.id
#GROUP BY o.customer_id, o.product, c.name, o.order_date;
#""")

#revised

# 3.1 Total Order Amount for each Customer
cursor.execute("""
SELECT
  o.customer_id,
  c.name,
  o.product,
  CAST(o.amount AS DECIMAL(7,2)) AS amount,
  o.order_date,
  SUM(CAST(o.amount AS DECIMAL(7,2))) AS total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
GROUP BY o.customer_id, o.product, c.name, o.order_date;
""")

data = cursor.fetchall()
#print(data)
print ("Using INNER JOIN to include customer with orders!")
df = pd.DataFrame(data, columns=["customer_id", "name", "product", "amount", "order_date", "total_amount"])
#print(df)

df["total_amount"] = df["amount"].apply(lambda x: f"₱{x:.2f}")
print(df)

# 3.1 Write a query to fetch customer information along with their total amount, using a LEFT JOIN to include customers without orders.

cursor.execute("""
SELECT c.id, c.name, c.email, coalesce(SUM(o.amount), 0) AS total_amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY c.id
""")

data = cursor.fetchall()
#print(data)

print ("Using LEFT JOIN to include customer without orders!")
df = pd.DataFrame(data, columns=["id", "name", "email", "total_amount"])
df["total_amount"] = df["total_amount"].apply(lambda x: f"₱{x:.2f}")
print(df)

#df["total_amount"] = df["amount"].apply(lambda x: f"₱{x:.2f}")
#print(df)


# 3.2 Implement a subquery to identify customers who have made transactions of more than PHP 5,000 in total.

cursor.execute("""
SELECT *
FROM customers c
WHERE c.id IN (
	SELECT customer_id
	FROM orders o
	GROUP BY customer_id
	HAVING SUM(amount) > 5000
);
""")

data = cursor.fetchall()
#print(data)

print (" Customer with more than PHP 5,000.00")
df = pd.DataFrame(data, columns=["customer_id", "name", "email"])
print(df)


cursor.execute("""
CREATE OR REPLACE FUNCTION calculate_discount(amount REAL)
RETURNS REAL
BEGIN
  DECLARE discount REAL;
  SET discount = amount * 0.5;
  
  -- Check if transaction date is within the last 30 days
  IF DATETIME('now') - INTERVAL 30 DAY <= transaction_date THEN
    SET discount = discount + (amount * 0.05);
  END IF;
  
  RETURN discount;
END;
""")

# Update existing records and insert new records with transaction dates
cursor.execute("""
UPDATE Orders SET transaction_date = DATETIME('now')
WHERE transaction_date IS NULL;
""")

cursor.execute("""
INSERT INTO Orders (customer_id, product, amount, order_date, transaction_date)
VALUES (2, 'Buko Pandan', 45.00, DATETIME('now'), DATETIME('now'));
""")

conn.commit()

# Calculate discounted amount for all orders with transaction dates
cursor.execute("""
SELECT product, calculate_discount(amount) AS discounted_amount, transaction_date
FROM Orders;
""")

products_with_discounts = cursor.fetchall()

