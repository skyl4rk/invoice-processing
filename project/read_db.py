import sqlite3

db_path = "../db/invoices.db"

# db_path = "../db/shipping_lists.db"
#
#  Check the data
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Invoices:")
for row in cursor.execute("SELECT * FROM invoices"):
    print(row)

print("\nProducts:")
for row in cursor.execute("SELECT * FROM products"):
    print(row)

conn.close()
