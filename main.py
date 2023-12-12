
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("sales.db")
c = conn.cursor()

# Define a stored procedure to calculate discount
#def calculate_discount(order_id, discount_code):
#    c.execute("SELECT discount_rate FROM discounts WHERE code = ?", (discount_code,))
#    discount_rate = c.fetchone()[0]
#    c.execute("SELECT SUM(price * quantity) FROM orders o INNER JOIN products p ON o.product_ID = p.ID WHERE o.ID = ?", (order_id,))
#    total_amount = c.fetchone()[0]
#    discount_amount = total_amount * discount_rate
#    return total_amount, discount_amount

# Get all orders with customer details and product names
c.execute("""
SELECT o.ID AS order_id, 
       c.name AS customer_name, 
       p.name AS product_name, 
       q.quantity, 
       d.order_date, 
       o.customer_ID, 
       r.product_ID,
       s.price
FROM orders o, order_items q, orders d, order_items r, products s
INNER JOIN customers c ON o.customer_ID = c.ID
INNER JOIN products p ON r.product_ID = p.ID
ORDER BY o.order_date DESC
""")

#c.execute("""
#SELECT c.name AS customer_name, o.order_date, oi.product_name, oi.quantity, oi.price, o.total_amount
#FROM orders o
#INNER JOIN customers c ON c.id = o.customer_id
##INNER JOIN order_items oi ON oi.order_id = o.id
#INNER JOIN products p ON p.id = oi.product_id
#ORDER BY o.order_date DESC
#""")






data = c.fetchall()
#print(data)

# Create pandas dataframe
df = pd.DataFrame(data, columns=["order_id", "customer_name", "product_name", "quantity", "date", "customer_ID", "product_ID", "price"])
#print(df)

# Calculate total amount and format currency
#price = df.apply(lambda row: float(c.execute("SELECT price FROM products WHERE ID = ?", (row["product_ID"],)).fetchone()[0]), axis=1)
df["total_amount"] = df["quantity"] * df.apply(lambda row: float(c.execute("SELECT price FROM products WHERE ID = ?", (row["product_ID"],)).fetchone()[0]), axis=1)
df["total_amount_formatted"] = df["total_amount"].apply(lambda x: f"₱{x:.2f}")

# Calculate discount using stored procedure
#df["discount_code"] = ""
#df["total_amount_with_discount"] = df["total_amount"]
#df["discount_amount"] = 0
#for i in range(len(df)):
#    discount_code = input(f"Enter discount code for order {df.loc[i, 'order_id']} (or leave empty): ")
#    df.loc[i, "discount_code"] = discount_code
#    if discount_code:
#        total_amount, discount_amount = calculate_discount(df.loc[i, "order_id"], discount_code)
#        df.loc[i, "total_amount"] = total_amount
#        df.loc[i, "discount_amount"] = discount_amount
#        df.loc[i, "total_amount_with_discount"] = total_amount - discount_amount
#    df.loc[i, "total_amount_with_discount_formatted"] = f"₱{df.loc[i, 'total_amount_with_discount']:.2f}"
#    df.loc[i, "discount_amount_formatted"] = f"₱{df.loc[i, 'discount_amount']:.2f}"

# Display the dashboard
#print("Sales Dashboard:")
#print(df.to_string())
print("Sales Dashboard")
print("----------------")
print("      Customer    |  Order Date   |   Product   |  Quantity  |  Price  |   Total")
print("      ---------   | ------------  |  ---------  | ---------- | ------- |  ------- ")
df.to_string(index=False, justify='center', col_space=10)
#print(df[["customer_name", "date", "product_name", "quantity", "price", "total_amount_formatted"]])
#df[["customer_name", "date", "product_name", "quantity", "price", "total_amount_formatted"]].apply(pd.Series.str.pad, width=25)
#print(df)
#print(f"{df['customer_name']:25s}{df['date']:15s}{df['product_name']:20s}{df['quantity']:5s}{df['price']:10s}{df['total_amount_formatted']}")
print(df.to_string())

# Close the database connection
conn.close()