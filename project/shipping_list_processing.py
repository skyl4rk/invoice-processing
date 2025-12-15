from PyPDF2 import PdfReader
from openai import OpenAI
import json
import sqlite3
from pydantic import BaseModel
from typing import List


def pdf_reader(doc_path):
    # PyPDF2 output: pdf to text
    reader = PdfReader(doc_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text


def structured_output(payload, key):
    # Pydantic models for structured output
    class Product(BaseModel):
        product_number: str
        description: str
        quantity: int

    class Shipping_List(BaseModel):
        shipping_date: str
        delivery_date: str
        invoice_number: str
        invoice_date: str
        products: List[Product]

    # call ai request json formatted output of invoice details
    prompt = f"Please extract the shipping date, delivery date, invoice number, invoice date, product number, description, and quantity from {payload}. Format as json. For date data, use the format MM/DD/YYYY."
    client = OpenAI(api_key=key)
    response = client.responses.parse(
        model="gpt-5-nano", input=prompt, text_format=Shipping_List
    )
    # print(response.output_text)
    return response.output_text


def save_to_sqlite(ship_data: dict, db_path: str = "../db/shipping_lists.db"):
    ship_data = json.loads(ship_data)

    """Create tables and insert invoice/products data into SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipping_lists (
            shipping_date TEXT,
            delivery_date TEXT,
            invoice_number TEXT PRIMARY KEY,
            invoice_date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_number TEXT,
            description TEXT,
            quantity INTEGER,
            invoice_number TEXT, 
            FOREIGN KEY (invoice_number) REFERENCES shipping_lists (invoice_number)
        )
    """)

    # Check if shipping list already exists
    cursor.execute(
        "SELECT 1 FROM shipping_lists WHERE invoice_number = ?",
        (ship_data["invoice_number"],),
    )
    if cursor.fetchone():
        print(
            f"⚠️ Shipping List {ship_data['invoice_number']} already exists, skipping."
        )
        conn.close()
        return False

    # Insert shipping list
    cursor.execute(
        """
        INSERT OR IGNORE INTO shipping_lists (shipping_date, delivery_date, invoice_number, invoice_date)
        VALUES (?, ?, ?, ?)
    """,
        (
            ship_data["shipping_date"],
            ship_data["delivery_date"],
            ship_data["invoice_number"],
            ship_data["invoice_date"],
        ),
    )

    # Insert each product
    for product in ship_data["products"]:
        cursor.execute(
            """
            INSERT INTO products (product_number, description, quantity, invoice_number)
            VALUES (?, ?, ?, ?)
        """,
            (
                product["product_number"],
                product["description"],
                product["quantity"],
                ship_data["invoice_number"],
            ),
        )

    conn.commit()
    conn.close()
    print(
        f"✅ Shipping List {ship_data['invoice_number']} saved with {len(ship_data['products'])} products."
    )
