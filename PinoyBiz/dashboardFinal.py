import sqlite3
import pandas as pd
import time as time


# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect("pinoybiz_sales1.db")

# Create cursor object
cursor = conn.cursor()

# 3. Dashboard Queries:

# 3.1 Total Order Amount for each Customer
print("\n3.1 Total Order Amount for each Customer")
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
print ("\n\n Using INNER JOIN to include customer with orders!")
df = pd.DataFrame(data, columns=["customer_id", "name", "product", "amount", "order_date", "total_amount"])
# Apply lambda function to format total amount with currency symbol
df["total_amount"] = df["amount"].apply(lambda x: f"₱{x:.2f}")
print(df)

# 3.1 Write a query to fetch customer information along with their total amount, using a LEFT JOIN to include customers without orders.
print("\n3.1 Write a query to fetch customer information along with their total amount, using a LEFT JOIN to include customers without orders.")
cursor.execute("""
SELECT c.id, c.name, c.email, coalesce(SUM(o.amount), 0) AS total_amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY c.id
""")

data = cursor.fetchall()

print ("\n\n Using LEFT JOIN to include customer without orders!")
df = pd.DataFrame(data, columns=["id", "name", "email", "total_amount"])
# Apply lambda function to format total amount with currency symbol
df["total_amount"] = df["total_amount"].apply(lambda x: f"₱{x:.2f}")
print(df)

# 3.2 Implement a subquery to identify customers who have made transactions of more than PHP 5,000 in total.
print("\n3.2 Implement a subquery to identify customers who have made transactions of more than PHP 5,000 in total.")
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
print (" Customer with more than PHP 5,000.00")
df = pd.DataFrame(data, columns=["customer_id", "name", "email"])
print(df)

# 3.3 Create a query to display the product, discounted amount (using the calculate_discount stored procedure), and transactions date for all orders.
print("\n3.3 Create a query to display the product, discounted amount (using the calculate_discount stored procedure), and transactions date for all orders.")
# Stored Procedure Function for the SQL to perform the discounted amount with Transaction Date
def calculate_discount(amount):
  """
  Calculates a discount of 5% on the provided amount.
  """
  try:
    discount = amount * 0.05
    discounted = amount - discount
    return discounted
  except Exception as e:
    # Handle the exception
    print(f"Error calculating discount: {e}")
    return None
  finally:
    # Cleanup resources (if necessary)
    pass

conn.create_function("calculate_discount", 1, calculate_discount)

cursor.execute("""
SELECT o.product, calculate_discount(o.amount) AS discounted_amount, t.transaction_date
FROM orders o
INNER JOIN transactions t ON o.id = t.id;
""")

#cursor.execute("SELECT 1 FROM sqlite_master WHERE type='function'")
data = cursor.fetchall()
print("\n\n Products with 0.05 discount with transaction date")
df = pd.DataFrame(data, columns=["PRODUCTS", "discounted", "TRANSACTION_DATE"])
df["discounted"] = df["discounted"].apply(lambda x: f"₱{x:.2f}")
print(df)

# 4. Indexing and Optimization:
print("\n4. Indexing and Optimization:")
# 4.1 Add an index to the order_date column in the Orders table to optimize queries related to date-based filtering, considering the importance of timely transactions in the local market

# Add index to order_date
#cursor.execute("CREATE INDEX idx_order_date ON Orders (order_date);")


# Demonstrate improved performance
start_time = time.time()
cursor.execute("SELECT * FROM Orders WHERE order_date = '2023-12-06';")
results = cursor.fetchall()
end_time = time.time()

print(f"Query execution time with index: {end_time - start_time}")


# 5. Transactions:
# Begin a transaction to update the order amount for a specific order, ensuring the scenario aligns with a local business context.
# If the updated amount exceeds a predefined threshold (e.g., PHP 10,000), you are required to roll back the transaction. Otherwise, you should commit the transaction.
print("\n5. Transactions:")
order_id = 1
new_amount = 11000
cursor.execute(f"SELECT amount FROM Orders WHERE id = {order_id};")
current_amount = cursor.fetchone()[0]
print(current_amount)

if new_amount > 10000:
  # Rollback transaction if exceeding threshold
  conn.rollback()
  print(f"Order amount update failed: exceeded threshold of PHP 10,000")
else:
  # Proceed with update
  cursor.execute(f"UPDATE Orders SET amount = {new_amount} WHERE id = {order_id};")
  conn.commit()
  print(f"Order amount updated successfully to PHP {new_amount}")




  