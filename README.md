# Local-Business-Sales-Dashboard
Local Business Sales Dashboard

In this activity, you will apply your knowledge of advanced SQL techniques with SQLite3 in Python to create a sales dashboard for a fictional local business in the Philippines. The dashboard should provide insights into customer orders, calculate discounts using stored procedures, and showcase transaction data tailored to the Filipino market.

Tasks:

Database Setup:

You are tasked with creating a SQLite database named 'PinoyBiz_Sales.db'.
You need to design and create tables for customers, orders, and transactions, incorporating fields such as customer_id, customer_name, email, order_id, product, amount, order_date, transaction_id, and transaction_date.
Data Population:

Insert sample data into the Customers, Orders, and Transactions tables, making sure to use Filipino names and products to create a dataset that reflects the local market.
Diversity in transactions is essential, ensuring various customers make multiple orders and transactions.
Dashboard Queries:

Write a query to fetch customer information along with their total order amount, using a LEFT JOIN to include customers without orders.
Implement a subquery to identify customers who have made transactions of more than PHP 5,000 in total.
Create a query to display the product, discounted amount (using the calculate_discount stored procedure), and transaction date for all orders.
Indexing and Optimization:

Add an index to the order_date column in the Orders table to optimize queries related to date-based filtering, considering the importance of timely transactions in the local market.
Write a query to demonstrate the improved performance after indexing.
Transactions:

Begin a transaction to update the order amount for a specific order, ensuring the scenario aligns with a local business context.
If the updated amount exceeds a predefined threshold (e.g., PHP 10,000), you are required to roll back the transaction. Otherwise, you should commit the transaction.
Stored Procedure Enhancement:

Modify the calculate_discount stored procedure to include an additional discount of 5% for transactions made within the last 30 days, reflecting local promotions.
Update existing records and insert new records to reflect the changes.
Triggers:

Create a trigger that updates the transaction_date in the Transactions table whenever a new order is inserted into the Orders table, aligning with local business practices.
Insert a new order and observe the automatic update of the transaction_date in the Transactions table.


FILES:
1. README.md 
2. pinoybiz_sales.py - dashboard task 3 to 7
3. dbcreateandpopulate.py - to create database, need to run this first before pinoybiz_sales.py
3. localbusinessalesdashboard.png - erd
4. pinoybiz_sales.db - database to be created by