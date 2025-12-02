import sqlite3
import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, ValidationError
import fitz  # PyMuPDF
from openai import OpenAI
import json
# import pandas as pd

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


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


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from the first page of the PDF."""
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    text = page.get_text()
    doc.close()
    print("✅ PDF text extracted.")
    return text


def parse_invoice_with_ai(text: str) -> dict:
    """Use AI to extract structured invoice data as JSON."""
    prompt = f"""
    Analyze this invoice text and extract the following in VALID JSON format ONLY (no extra text/comments):
    Text: {text}
    """

    response = client.responses.parse(
        model="gpt-5-nano",
        input=prompt,
        text_format=Invoice,
        #    max_tokens=100,
    )

    json_str = response.choices[0].message.content
    print(
        "✅ AI parsed JSON:",
    )

    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"AI output is not valid JSON: {e}")


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
        invoice = Invoice(**invoice_data)
        cursor.execute(
            "INSERT OR REPLACE INTO invoices (invoice_number, invoice_date, total) VALUES (?, ?, ?)",
            (invoice.invoice_number, invoice.invoice_date, invoice.total),
        )
    except ValidationError as e:
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
