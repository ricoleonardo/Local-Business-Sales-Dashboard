import sqlite3

# Connect to the database
conn = sqlite3.connect("sales.db")

# Define a function to calculate the discount based on total amount
def calculate_discount(total_amount):
  if total_amount >= 1000:
    return total_amount * 0.10
  else:
    return 0

# Create a stored procedure to apply the discount
conn.execute("""
CREATE OR REPLACE PROCEDURE apply_discount(
  @total_amount DECIMAL(7,2)
)
AS BEGIN
  UPDATE orders SET total_amount = @total_amount - calculate_discount(@total_amount);
END;
""")

# Apply discount to all orders
cursor = conn.cursor()
cursor.execute("SELECT id, total_amount FROM orders")
for order_id, total_amount in cursor.fetchall():
  conn.callproc("apply_discount", (total_amount,))

# Fetch data for the dashboard
cursor.execute("""
SELECT c.name AS customer_name, o.order_date, oi.product_name, oi.quantity, oi.price, o.total_amount
FROM orders o
INNER JOIN customers c ON c.id = o.customer_id
INNER JOIN order_items oi ON oi.order_id = o.id
INNER JOIN products p ON p.id = oi.product_id
ORDER BY o.order_date DESC
""")

data = cursor.fetchall()

# Close the connection
conn.commit()
conn.close()

# Display the dashboard
print("Sales Dashboard")
print("----------------")
print("Customer | Order Date | Product | Quantity | Price | Total")
print("---------|------------|---------|----------|-------|-------")
for customer_name, order_date, product_name, quantity, price, total_amount in data:
  print(f
