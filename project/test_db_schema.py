import sqlite3

db_path = "../db/shipping_lists.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(shipping_lists)")
print(cursor.fetchall())
cursor.execute("PRAGMA table_info(products)")
print(cursor.fetchall())
conn.close()
