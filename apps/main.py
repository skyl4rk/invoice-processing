# import sqlite3
import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, ValidationError

# import fitz  # PyMuPDF
from openai import OpenAI

# import json
import pandas as pd
import invoice as inv


# Load environment variables
# load_dotenv()
# api_key = os.getenv("API_KEY")
# client = OpenAI(api_key=api_key)


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


if __name__ == "__main__":
    pdf_path = "../data/invoices_pdf/202501-invoice.pdf"  # Update path to your PDF

    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        exit(1)

    try:
        text = inv.extract_pdf_text(pdf_path)

        print("text output:")
        print(text)

        invoice_data = inv.parse_invoice_with_ai(text)
        inv.save_to_sqlite(invoice_data)

        # Query to verify
        conn = inv.sqlite3.connect("../db/invoices.db")
        print("\n📊 Invoices table:")
        print(pd.read_sql_query("SELECT * FROM invoices", conn))
        print("\n📦 Products table:")
        print(pd.read_sql_query("SELECT * FROM products", conn))
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")
