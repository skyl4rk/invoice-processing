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
        unit_price: float
        amount: float

    class Invoice(BaseModel):
        invoice_number: str
        invoice_date: str
        products: List[Product]
        total: float

    # call ai request json formatted output of invoice details
    prompt = f"Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from {payload}. Format as json."
    client = OpenAI(api_key=key)
    response = client.responses.parse(
        model="gpt-5-nano", input=prompt, text_format=Invoice
    )
    # print(response.output_text)
    return response.output_text


def save_to_sqlite(invoice_data: dict, db_path: str = "../db/invoices.db"):
    invoice_data = json.loads(invoice_data)

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

    # Check if invoice already exists
    cursor.execute(
        "SELECT 1 FROM invoices WHERE invoice_number = ?",
        (invoice_data["invoice_number"],),
    )
    if cursor.fetchone():
        print(f"⚠️ Invoice {invoice_data['invoice_number']} already exists, skipping.")
        conn.close()
        return False

    # Insert invoice
    cursor.execute(
        """
        INSERT OR IGNORE INTO invoices (invoice_number, invoice_date, total)
        VALUES (?, ?, ?)
    """,
        (
            invoice_data["invoice_number"],
            invoice_data["invoice_date"],
            invoice_data["total"],
        ),
    )

    # Insert each product
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

    conn.commit()
    conn.close()
    print(
        f"✅ Invoice {invoice_data['invoice_number']} saved with {len(invoice_data['products'])} products."
    )
