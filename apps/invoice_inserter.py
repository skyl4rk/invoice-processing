import sqlite3


txt = """
{
  "invoice_number": "25011",
  "invoice_date": "1/24/2019",
  "products": [
    {
      "product_number": "95064",
      "description": "White Flour Natural, Premium, Unbleached, 50lb",
      "quantity": 1,
      "unit_price": 184.95,
      "amount": 84.95
    },
    {
      "product_number": "95073",
      "description": "Cake Flour, Premium 50lb",
      "quantity": 1,
      "unit_price": 196.95,
      "amount": 96.95
    },
    {
      "product_number": "240206",
      "description": "Shortening, Organic, All-Vegetable, 24 oz",
      "quantity": 1,
      "unit_price": 117.95,
      "amount": 17.95
    },
    {
      "product_number": "210241",
      "description": "Sugar, Powdered Confectioners, 5X, 50lb",
      "quantity": 1,
      "unit_price": 198.95,
      "amount": 98.95
    },
    {
      "product_number": "232054",
      "description": "Raspberry Preserves, Organic 15lb",
      "quantity": 1,
      "unit_price": 165.95,
      "amount": 65.95
    },
    {
      "product_number": "271674",
      "description": "Cacao, Organic, 20lb",
      "quantity": 1,
      "unit_price": 156.95,
      "amount": 56.95
    },
    {
      "product_number": "393959",
      "description": "Milk, Homogenized, 1 gallon",
      "quantity": 1,
      "unit_price": 14.95,
      "amount": 4.95
    },
    {
      "product_number": "548848",
      "description": "Eggs, Grade A, 24 eggs",
      "quantity": 1,
      "unit_price": 112.95,
      "amount": 12.95
    },
    {
      "product_number": "437894",
      "description": "Baking Powder, 1lb",
      "quantity": 1,
      "unit_price": 122.95,
      "amount": 22.95
    },
    {
      "product_number": "654445",
      "description": "Salt, 5lb",
      "quantity": 1,
      "unit_price": 19.95,
      "amount": 9.95
    },
    {
      "product_number": "893798",
      "description": "Aprons, Bakery, Large",
      "quantity": 1,
      "unit_price": 119.95,
      "amount": 19.95
    },
    {
      "product_number": "908098",
      "description": "Cake Pan, 9\" x 17\"",
      "quantity": 1,
      "unit_price": 119.95,
      "amount": 19.95
    }
  ],
  "total": 512.40
}
"""


def save_to_sqlite(invoice_data: dict, db_path: str = "../db/invoices.db"):
    """Create tables and insert invoice/products data into SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_number TEXT PRIMARY KEY,
            invoice_date TEXT,
            total REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_number TEXT,
            description TEXT,
            quantity INTEGER,
            unit_price REAL,
            amount REAL,
            invoice_number TEXT,
            FOREIGN KEY (invoice_number) REFERENCES invoices (invoice_number)
        )
    """)

    # Validate and insert invoice
    try:
        invoice = invoices(**invoice_data)
        cursor.execute(
            "INSERT OR REPLACE INTO invoices (invoice_number, invoice_date, total) VALUES (?, ?, ?)",
            (invoice.invoice_number, invoice.invoice_date, invoice.total),
        )
    except Exception as e:
        print(f"❌ Validation error: {e}")
        conn.close()
        return

    # Insert products
    for product in invoice.products:
        cursor.execute(
            "INSERT OR IGNORE INTO products (product_number, description, quantity, unit_price, amount, invoice_number) VALUES (?, ?, ?, ?, ?, ?)",
            (
                product.product_number,
                product.description,
                product.quantity,
                product.unit_price,
                product.amount,
                invoice.invoice_number,
            ),
        )

    conn.commit()
    conn.close()
    print(f"✅ Data saved to {db_path}")
