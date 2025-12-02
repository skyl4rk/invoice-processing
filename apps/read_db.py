import sqlite3

# Check the data
conn = sqlite3.connect("../db/invoices.db")
cursor = conn.cursor()

print("Invoices:")
for row in cursor.execute("SELECT * FROM invoices"):
    print(row)

print("\nProducts:")
for row in cursor.execute("SELECT * FROM products"):
    print(row)

conn.close()
