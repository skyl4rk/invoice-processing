import sqlite3


connection_obj = sqlite3.connect("../db/invoices.db")

cursor_obj = connection_obj.cursor()

statement = """SELECT * FROM invoices"""

cursor_obj.execute(statement)

print("Data rows:")
output = cursor_obj.fetchall()
for row in output:
    print(row)

connection_obj.commit()

connection_obj.close()
