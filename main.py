
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("sales.db")
c = conn.cursor()

# Define a stored procedure to calculate discount
def calculate_discount(order_id, discount_code):
    c.execute("SELECT discount_rate FROM discounts WHERE code = ?", (discount_code,))
    discount_rate = c.fetchone()[0]
    c.execute("SELECT SUM(price * quantity) FROM orders o INNER JOIN products p ON o.product_ID = p.ID WHERE o.ID = ?", (order_id,))
    total_amount = c.fetchone()[0]
    discount_amount = total_amount * discount_rate
    return total_amount, discount_amount

# Get all orders with customer details and product names
c.execute("""
SELECT o.ID AS order_id, c.name AS customer_name, p.name AS product_name, o.quantity, o.date, o.customer_ID, o.product_ID
FROM orders o
INNER JOIN customers c ON o.customer_ID = c.ID
INNER JOIN products p ON o.product_ID = p.ID
""")
data = c.fetchall()

# Create pandas dataframe
df = pd.DataFrame(data, columns=["order_id", "customer_name", "product_name", "quantity", "date", "customer_ID", "product_ID"])

# Calculate total amount and format currency
df["total_amount"] = df["quantity"] * df.apply(lambda row: float(c.execute("SELECT price FROM products WHERE ID = ?", (row["product_ID"],)).fetchone()[0]), axis=1)
df["total_amount_formatted"] = df["total_amount"].apply(lambda x: f"₱{x:.2f}")

# Calculate discount using stored procedure
df["discount_code"] = ""
df["total_amount_with_discount"] = df["total_amount"]
df["discount_amount"] = 0
for i in range(len(df)):
    discount_code = input(f"Enter discount code for order {df.loc[i, 'order_id']} (or leave empty): ")
    df.loc[i, "discount_code"] = discount_code
    if discount_code:
        total_amount, discount_amount = calculate_discount(df.loc[i, "order_id"], discount_code)
        df.loc[i, "total_amount"] = total_amount
        df.loc[i, "discount_amount"] = discount_amount
        df.loc[i, "total_amount_with_discount"] = total_amount - discount_amount
    df.loc[i, "total_amount_with_discount_formatted"] = f"₱{df.loc[i, 'total_amount_with_discount']:.2f}"
    df.loc[i, "discount_amount_formatted"] = f"₱{df.loc[i, 'discount_amount']:.2f}"

# Display the dashboard
print("Sales Dashboard:")
print(df.to_string())

# Close the database connection
conn.close()