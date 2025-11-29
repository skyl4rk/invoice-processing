import sqlite3

# Dictionary with invoice data
invoice_dict = {
    "invoice_number": "2034",
    "invoice_date": "1/1/2025",
    "products": [
        {
            "product_number": "95064",
            "description": "White Flour Natural, Premium, Unbleached, 50lb",
            "quantity": 1,
            "unit_price": 84.95,
            "amount": 84.95,
        },
        {
            "product_number": "95073",
            "description": "Cake Flour, Premium 50lb",
            "quantity": 1,
            "unit_price": 96.95,
            "amount": 96.95,
        },
        {
            "product_number": "240206",
            "description": "Shortening, Organic, All-Vegetable, 24 oz",
            "quantity": 1,
            "unit_price": 17.95,
            "amount": 17.95,
        },
        {
            "product_number": "210241",
            "description": "Sugar, Powdered Confectioners, 5X, 50lb",
            "quantity": 1,
            "unit_price": 98.95,
            "amount": 98.95,
        },
        {
            "product_number": "232054",
            "description": "Raspberry Preserves, Organic 15lb",
            "quantity": 1,
            "unit_price": 65.95,
            "amount": 65.95,
        },
        {
            "product_number": "271674",
            "description": "Cacao, Organic, 20lb",
            "quantity": 1,
            "unit_price": 56.95,
            "amount": 56.95,
        },
        {
            "product_number": "393959",
            "description": "Milk, Homogenized, 1 gallon",
            "quantity": 1,
            "unit_price": 4.95,
            "amount": 4.95,
        },
        {
            "product_number": "548848",
            "description": "Eggs, Grade A, 24 eggs",
            "quantity": 1,
            "unit_price": 12.95,
            "amount": 12.95,
        },
        {
            "product_number": "437894",
            "description": "Baking Powder, 1lb",
            "quantity": 1,
            "unit_price": 22.95,
            "amount": 22.95,
        },
        {
            "product_number": "654445",
            "description": "Salt, 5lb",
            "quantity": 1,
            "unit_price": 9.95,
            "amount": 9.95,
        },
        {
            "product_number": "893798",
            "description": "Aprons, Bakery, Large",
            "quantity": 1,
            "unit_price": 19.95,
            "amount": 19.95,
        },
        {
            "product_number": "908098",
            "description": "Cake Pan, 9” x 17”",
            "quantity": 1,
            "unit_price": 19.95,
            "amount": 19.95,
        },
    ],
    "total": 512.40,
}

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("../db/invoices.db")
cursor = conn.cursor()

# Create the invoices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    invoice_number TEXT PRIMARY KEY,
    invoice_date TEXT,
    total REAL
)
""")

# Create the products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_number TEXT PRIMARY KEY,
    description TEXT,
    quantity INTEGER,
    unit_price REAL,
    amount REAL,
    invoice_number TEXT,
    FOREIGN KEY (invoice_number) REFERENCES invoices (invoice_number)
)
""")

# Commit the changes
conn.commit()

# Insert the invoice data
invoice_data = invoice_dict
cursor.execute(
    """
INSERT INTO invoices (invoice_number, invoice_date, total)
VALUES (?, ?, ?)
""",
    (
        invoice_data["invoice_number"],
        invoice_data["invoice_date"],
        invoice_data["total"],
    ),
)

# Insert the product data
for product in invoice_data["products"]:
    cursor.execute(
        """
    INSERT INTO products (product_number, description, quantity, unit_price, amount, invoice_number)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            product["product_number"],
            product["description"],
            product["quantity"],
            product["unit_price"],
            product["amount"],
            invoice_data["invoice_number"],
        ),
    )

# Commit the changes
conn.commit()

# Close the connection
conn.close()
